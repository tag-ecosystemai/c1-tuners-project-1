from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models

from ai.data.detector_dataset import create_detector_dataloaders


MODEL_DIR = Path("ai/models/detector")
MODEL_PATH = MODEL_DIR / "potato_detector_best.pth"

EPOCHS = 10
LEARNING_RATE = 0.0001


def main():

    device = (
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    print(f"Using device: {device}")

    # Load detector dataset
    (
        train_loader,
        val_loader,
        test_loader,
        classes
    ) = create_detector_dataloaders()

    print(f"Classes: {classes}")

    # Load pretrained ResNet18
    weights = models.ResNet18_Weights.DEFAULT

    model = models.resnet18(
        weights=weights
    )

    # Freeze early layers
    for param in model.parameters():
        param.requires_grad = False

    # Replace final classifier
    model.fc = nn.Linear(
        model.fc.in_features,
        2
    )

    # Only classifier is trainable
    for param in model.fc.parameters():
        param.requires_grad = True

    model = model.to(device)

    # Loss
    criterion = nn.CrossEntropyLoss()

    # Optimizer
    optimizer = optim.Adam(
        model.fc.parameters(),
        lr=LEARNING_RATE
    )

    best_val_accuracy = 0.0

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    for epoch in range(EPOCHS):

        # ==============================
        # Training
        # ==============================

        model.train()

        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:

            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = model(images)

            loss = criterion(
                outputs,
                labels
            )

            loss.backward()
            optimizer.step()

            running_loss += (
                loss.item() * images.size(0)
            )

            _, predicted = torch.max(
                outputs,
                1
            )

            total += labels.size(0)

            correct += (
                predicted == labels
            ).sum().item()

        train_loss = (
            running_loss / total
        )

        train_accuracy = (
            correct / total
        ) * 100

        # ==============================
        # Validation
        # ==============================

        model.eval()

        val_correct = 0
        val_total = 0
        val_loss_total = 0.0

        with torch.no_grad():

            for images, labels in val_loader:

                images = images.to(device)
                labels = labels.to(device)

                outputs = model(images)

                loss = criterion(
                    outputs,
                    labels
                )

                val_loss_total += (
                    loss.item()
                    * images.size(0)
                )

                _, predicted = torch.max(
                    outputs,
                    1
                )

                val_total += labels.size(0)

                val_correct += (
                    predicted == labels
                ).sum().item()

        val_loss = (
            val_loss_total / val_total
        )

        val_accuracy = (
            val_correct / val_total
        ) * 100

        print(
            f"\nEpoch [{epoch + 1}/{EPOCHS}]"
        )

        print(
            f"Train Loss: {train_loss:.4f}"
        )

        print(
            f"Train Acc: {train_accuracy:.2f}%"
        )

        print(
            f"Val Loss: {val_loss:.4f}"
        )

        print(
            f"Val Acc: {val_accuracy:.2f}%"
        )

        # Save best model
        if val_accuracy > best_val_accuracy:

            best_val_accuracy = val_accuracy

            torch.save(
                model.state_dict(),
                MODEL_PATH
            )

            print(
                f"⭐ New best model! "
                f"Validation Accuracy: "
                f"{val_accuracy:.2f}%"
            )

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)

    print(
        f"Best Validation Accuracy: "
        f"{best_val_accuracy:.2f}%"
    )

    print(
        f"Best model saved to:"
        f"\n{MODEL_PATH}"
    )


if __name__ == "__main__":
    main()