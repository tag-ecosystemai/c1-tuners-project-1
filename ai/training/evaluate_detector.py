import torch
from torchvision import models
from sklearn.metrics import classification_report, confusion_matrix

from ai.data.detector_dataset import create_detector_dataloaders


MODEL_PATH = "ai/models/detector/potato_detector_best.pth"
THRESHOLD = 0.50


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load test data
    _, _, test_loader, class_names = create_detector_dataloaders()

    # Load model
    model = models.resnet18(weights=None)
    model.fc = torch.nn.Linear(model.fc.in_features, 2)

    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model = model.to(device)
    model.eval()

    all_predictions = []
    all_labels = []

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)

            outputs = model(images)
            probabilities = torch.softmax(outputs, dim=1)

            # Probability of potato_leaf (class 1)
            potato_probs = probabilities[:, 1]

            # Apply threshold
            predictions = (potato_probs >= THRESHOLD).long()

            all_predictions.extend(predictions.cpu().numpy())
            all_labels.extend(labels.numpy())

    # Confusion matrix
    cm = confusion_matrix(
        all_labels,
        all_predictions,
        labels=[0, 1]
    )

    print("\n" + "=" * 60)
    print("DETECTOR FINAL TEST RESULTS")
    print("=" * 60)

    print(f"\nThreshold: {THRESHOLD}")
    print("\nClasses:")
    for index, name in enumerate(class_names):
        print(f"{index} -> {name}")

    print("\nConfusion Matrix:")
    print(cm)

    print("\nClassification Report:")
    print(
        classification_report(
            all_labels,
            all_predictions,
            target_names=class_names,
            digits=4
        )
    )


if __name__ == "__main__":
    main()