from pathlib import Path

from torchvision import datasets
from torch.utils.data import DataLoader, Subset
from sklearn.model_selection import train_test_split

from .preprocessing import train_transform, val_test_transform


DETECTOR_DIR = (
    Path(__file__).resolve().parent / "detector"
)

BATCH_SIZE = 32
RANDOM_STATE = 42


def create_detector_dataloaders():

    base_dataset = datasets.ImageFolder(
        DETECTOR_DIR
    )

    labels = base_dataset.targets
    indices = list(range(len(base_dataset)))

    # 70% training, 30% temporary
    train_indices, temp_indices = train_test_split(
        indices,
        test_size=0.30,
        stratify=labels,
        random_state=RANDOM_STATE
    )

    temp_labels = [
        labels[i]
        for i in temp_indices
    ]

    # Split temporary into 15% validation
    # and 15% test
    val_indices, test_indices = train_test_split(
        temp_indices,
        test_size=0.50,
        stratify=temp_labels,
        random_state=RANDOM_STATE
    )

    # Separate datasets so transforms
    # don't interfere
    train_dataset_full = datasets.ImageFolder(
        DETECTOR_DIR,
        transform=train_transform
    )

    val_dataset_full = datasets.ImageFolder(
        DETECTOR_DIR,
        transform=val_test_transform
    )

    test_dataset_full = datasets.ImageFolder(
        DETECTOR_DIR,
        transform=val_test_transform
    )

    train_dataset = Subset(
        train_dataset_full,
        train_indices
    )

    val_dataset = Subset(
        val_dataset_full,
        val_indices
    )

    test_dataset = Subset(
        test_dataset_full,
        test_indices
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    return (
        train_loader,
        val_loader,
        test_loader,
        base_dataset.classes
    )