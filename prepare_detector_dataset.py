from pathlib import Path
import random
import shutil


SOURCE_DIR = Path("ai/data/raw/Dataset")
DEST_DIR = Path("ai/data/detector/potato_leaf")

IMAGES_PER_CLASS = {
    "Potato___Early_blight": 280,
    "Potato___Late_blight": 280,
    "Potato___healthy": 152,
}

RANDOM_SEED = 42

CLASSES = [
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
]

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


def main():

    random.seed(RANDOM_SEED)

    DEST_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    total_copied = 0

    for class_name in CLASSES:

        source_class_dir = SOURCE_DIR / class_name

        images = [
            path
            for path in source_class_dir.iterdir()
            if path.is_file()
            and path.suffix.lower() in IMAGE_EXTENSIONS
        ]

        required = IMAGES_PER_CLASS[class_name]
        if len(images) < required:
            raise ValueError(
                f"{class_name} only has {len(images)} images."
            )

        selected_images = random.sample(
            images,
            required
        )

        print(
            f"{class_name}: "
            f"selecting {required} images"
        )

        for image_path in selected_images:

            # Prefix filename with class name to avoid collisions
            destination_name = (
                f"{class_name}_{image_path.name}"
            )

            destination = DEST_DIR / destination_name

            shutil.copy2(
                image_path,
                destination
            )

            total_copied += 1

    print("\n" + "=" * 50)
    print("DETECTOR DATASET PREPARED")
    print("=" * 50)
    print(f"Potato leaf images: {total_copied}")
    print(f"Destination: {DEST_DIR}")


if __name__ == "__main__":
    main()