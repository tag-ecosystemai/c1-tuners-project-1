import torch
from torchvision import models
from sklearn.metrics import confusion_matrix

from ai.data.detector_dataset import create_detector_dataloaders


MODEL_PATH = "ai/models/detector/potato_detector_best.pth"


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load validation data
    _, val_loader, _, class_names = create_detector_dataloaders()

    # Load model
    model = models.resnet18(weights=None)
    model.fc = torch.nn.Linear(model.fc.in_features, 2)

    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model = model.to(device)
    model.eval()

    all_labels = []
    all_potato_probs = []

    # Get probabilities on validation set
    with torch.no_grad():
        for images, labels in val_loader:
            images = images.to(device)

            outputs = model(images)
            probabilities = torch.softmax(outputs, dim=1)

            # Class 1 = potato_leaf
            potato_probs = probabilities[:, 1]

            all_labels.extend(labels.numpy())
            all_potato_probs.extend(potato_probs.cpu().numpy())

    print("\n" + "=" * 70)
    print("DETECTOR THRESHOLD ANALYSIS")
    print("=" * 70)

    print(f"\nValidation images: {len(all_labels)}")
    print("\nClass mapping:")
    print("0 -> not_potato_leaf")
    print("1 -> potato_leaf")

    print("\n" + "-" * 70)
    print(
        f"{'Threshold':<12}"
        f"{'Accuracy':<12}"
        f"{'Potato Recall':<16}"
        f"{'False Positives':<18}"
        f"{'False Negatives':<18}"
    )
    print("-" * 70)

    for threshold in [0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.97, 0.99]:
        predictions = [
            1 if prob >= threshold else 0
            for prob in all_potato_probs
        ]

        cm = confusion_matrix(
            all_labels,
            predictions,
            labels=[0, 1]
        )

        tn, fp, fn, tp = cm.ravel()

        accuracy = (tn + tp) / len(all_labels)
        potato_recall = tp / (tp + fn) if (tp + fn) > 0 else 0

        print(
            f"{threshold:<12.2f}"
            f"{accuracy * 100:<12.2f}"
            f"{potato_recall * 100:<16.2f}"
            f"{fp:<18}"
            f"{fn:<18}"
        )


if __name__ == "__main__":
    main()