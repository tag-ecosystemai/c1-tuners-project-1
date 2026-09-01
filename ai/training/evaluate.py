import torch
from sklearn.metrics import classification_report, confusion_matrix

from ai.data.dataset import create_dataloaders
from ai.models.model import create_model



# CONFIGURATION

MODEL_PATH = "ai/models/weights/potato_resnet18_best.pth"



# DEVICE


device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Using device:", device)


# LOAD DATA

_, _, test_loader, classes = create_dataloaders()


# LOAD MODEL

model = create_model()

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=device
    )
)

model = model.to(device)

model.eval()


# EVALUATION

all_predictions = []
all_labels = []

correct = 0
total = 0


with torch.no_grad():

    for images, labels in test_loader:

        images = images.to(device)
        labels = labels.to(device)

        outputs = model(images)

        _, predictions = torch.max(
            outputs,
            1
        )

        total += labels.size(0)

        correct += (
            predictions == labels
        ).sum().item()

        all_predictions.extend(
            predictions.cpu().numpy()
        )

        all_labels.extend(
            labels.cpu().numpy()
        )

# TEST ACCURACY

test_accuracy = (
    100 * correct / total
)

print("\n" + "=" * 60)
print("TEST SET RESULTS")
print("=" * 60)

print(
    f"Test Accuracy: {test_accuracy:.2f}%"
)


# CLASSIFICATION REPORT

print("\n" + "=" * 60)
print("CLASSIFICATION REPORT")
print("=" * 60)

print(
    classification_report(
        all_labels,
        all_predictions,
        target_names=classes,
        digits=2
    )
)


# CONFUSION MATRIX

print("\n" + "=" * 60)
print("CONFUSION MATRIX")
print("=" * 60)

print(
    confusion_matrix(
        all_labels,
        all_predictions
    )
)