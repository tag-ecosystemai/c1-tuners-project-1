import copy
import torch
import torch.nn as nn
import torch.optim as optim

from ai.data.dataset import create_dataloaders
from ai.models.model import create_model


# =========================
# CONFIGURATION
# =========================

NUM_EPOCHS = 10
LEARNING_RATE = 0.0001

MODEL_SAVE_PATH = "ai/models/weights/potato_resnet18_best.pth"


# =========================
# DEVICE
# =========================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Using device:", device)


# =========================
# DATA
# =========================

train_loader, val_loader, test_loader, classes = create_dataloaders()

print("Classes:", classes)
print("Training images:", len(train_loader.dataset))
print("Validation images:", len(val_loader.dataset))
print("Test images:", len(test_loader.dataset))


# =========================
# MODEL
# =========================

model = create_model()

model = model.to(device)


# =========================
# LOSS FUNCTION
# =========================

criterion = nn.CrossEntropyLoss()


# =========================
# OPTIMIZER
# =========================

optimizer = optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE
)


# =========================
# TRAINING
# =========================

best_val_accuracy = 0.0
best_model_state = None


for epoch in range(NUM_EPOCHS):

    # -------------------------
    # TRAIN
    # -------------------------

    model.train()

    running_train_loss = 0.0
    correct_train = 0
    total_train = 0

    for images, labels in train_loader:

        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        running_train_loss += loss.item() * images.size(0)

        _, predicted = torch.max(outputs, 1)

        total_train += labels.size(0)

        correct_train += (
            predicted == labels
        ).sum().item()

    train_loss = running_train_loss / total_train

    train_accuracy = (
        100 * correct_train / total_train
    )


    # -------------------------
    # VALIDATION
    # -------------------------

    model.eval()

    running_val_loss = 0.0
    correct_val = 0
    total_val = 0

    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)

            loss = criterion(outputs, labels)

            running_val_loss += (
                loss.item() * images.size(0)
            )

            _, predicted = torch.max(outputs, 1)

            total_val += labels.size(0)

            correct_val += (
                predicted == labels
            ).sum().item()

    val_loss = running_val_loss / total_val

    val_accuracy = (
        100 * correct_val / total_val
    )


    # -------------------------
    # SAVE BEST MODEL
    # -------------------------

    if val_accuracy > best_val_accuracy:

        best_val_accuracy = val_accuracy

        best_model_state = copy.deepcopy(
            model.state_dict()
        )

        torch.save(
            best_model_state,
            MODEL_SAVE_PATH
        )

        print(
            f"⭐ New best model! "
            f"Validation Accuracy: "
            f"{best_val_accuracy:.2f}%"
        )


    # -------------------------
    # PRINT RESULTS
    # -------------------------

    print(
        f"Epoch [{epoch + 1}/{NUM_EPOCHS}] "
        f"Train Loss: {train_loss:.4f} "
        f"Train Acc: {train_accuracy:.2f}% "
        f"Val Loss: {val_loss:.4f} "
        f"Val Acc: {val_accuracy:.2f}%"
    )


print(
    f"\nBest Validation Accuracy: "
    f"{best_val_accuracy:.2f}%"
)

print(
    f"Best model saved to: "
    f"{MODEL_SAVE_PATH}"
)