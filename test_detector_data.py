from ai.data.detector_dataset import create_detector_dataloaders


def main():

    (
        train_loader,
        val_loader,
        test_loader,
        classes
    ) = create_detector_dataloaders()

    print("=" * 50)
    print("DETECTOR DATASET")
    print("=" * 50)

    print(f"Classes: {classes}")

    print(
        f"Training images: "
        f"{len(train_loader.dataset)}"
    )

    print(
        f"Validation images: "
        f"{len(val_loader.dataset)}"
    )

    print(
        f"Test images: "
        f"{len(test_loader.dataset)}"
    )

    images, labels = next(iter(train_loader))

    print(
        f"\nBatch image shape: "
        f"{images.shape}"
    )

    print(
        f"Batch label shape: "
        f"{labels.shape}"
    )


if __name__ == "__main__":
    main()