from pathlib import Path

from ai.inference.predict import predict


# ============================================================
# TEST DATA DIRECTORY
# ============================================================

TEST_DIR = Path("ai/data/external_test")


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n" + "=" * 70)
    print("FINAL INFERENCE PIPELINE TEST")
    print("=" * 70)

    image_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }

    # Loop through test categories
    for folder in sorted(TEST_DIR.iterdir()):

        if not folder.is_dir():
            continue

        print("\n" + "=" * 70)
        print(f"TEST CATEGORY: {folder.name}")
        print("=" * 70)

        images = [
            image
            for image in folder.iterdir()
            if image.suffix.lower() in image_extensions
        ]

        if not images:
            print("No images found.")
            continue

        # Test every image in the folder
        for image_path in images:

            print(f"\nImage: {image_path.name}")

            try:

                result = predict(image_path)

                # ====================================================
                # DETECTOR RESULTS
                # ====================================================

                print(
                    f"Potato leaf: "
                    f"{result['is_potato_leaf']}"
                )

                print(
                    f"Potato probability: "
                    f"{result['potato_probability'] * 100:.2f}%"
                )

                print(
                    f"Not-potato probability: "
                    f"{result['not_potato_probability'] * 100:.2f}%"
                )

                # ====================================================
                # REJECTED IMAGE
                # ====================================================

                if not result["is_potato_leaf"]:

                    print("Prediction: REJECTED")
                    print("Disease confidence: N/A")
                    print("Confidence level: N/A")

                    print(
                        f"\nExplanation:\n"
                        f"{result['explanation']}"
                    )

                    print(
                        f"\nRecommendation:\n"
                        f"{result['recommendation']}"
                    )

                # ====================================================
                # POTATO LEAF
                # ====================================================

                else:

                    print(
                        f"Prediction: "
                        f"{result['prediction']}"
                    )

                    print(
                        f"Disease confidence: "
                        f"{result['confidence'] * 100:.2f}%"
                    )

                    print(
                        f"Confidence level: "
                        f"{result['confidence_level'].upper()}"
                    )

                    print(
                        f"\nExplanation:\n"
                        f"{result['explanation']}"
                    )

                    print(
                        f"\nRecommendation:\n"
                        f"{result['recommendation']}"
                    )

            except Exception as e:

                print(f"ERROR: {e}")


# ============================================================
# RUN TEST
# ============================================================

if __name__ == "__main__":
    main()
