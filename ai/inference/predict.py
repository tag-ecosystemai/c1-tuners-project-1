import torch
from PIL import Image
from torchvision import models

from ai.models.model import create_model
from ai.data.preprocessing import val_test_transform
from ai.inference.explanations import generate_explanation


# ============================================================
# MODEL PATHS
# ============================================================

DISEASE_MODEL_PATH = "ai/models/weights/potato_resnet18_best.pth"
DETECTOR_MODEL_PATH = "ai/models/detector/potato_detector_best.pth"


# ============================================================
# CLASS NAMES
# ============================================================

DISEASE_CLASS_NAMES = [
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy"
]


# ============================================================
# DETECTOR THRESHOLD
# ============================================================

DETECTOR_THRESHOLD = 0.50


# ============================================================
# DEVICE
# ============================================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ============================================================
# LOAD DISEASE MODEL
# ============================================================

disease_model = create_model()

disease_model.load_state_dict(
    torch.load(
        DISEASE_MODEL_PATH,
        map_location=device
    )
)

disease_model = disease_model.to(device)
disease_model.eval()


# ============================================================
# LOAD POTATO LEAF DETECTOR
# ============================================================

detector_model = models.resnet18(weights=None)

detector_model.fc = torch.nn.Linear(
    detector_model.fc.in_features,
    2
)

detector_model.load_state_dict(
    torch.load(
        DETECTOR_MODEL_PATH,
        map_location=device
    )
)

detector_model = detector_model.to(device)
detector_model.eval()


# ============================================================
# PREDICT
# ============================================================

def predict(image_path):

    # Load image
    image = Image.open(image_path).convert("RGB")

    # Preprocess
    image_tensor = val_test_transform(image)

    # Add batch dimension
    image_tensor = image_tensor.unsqueeze(0)

    # Move to device
    image_tensor = image_tensor.to(device)

    # ========================================================
    # STEP 1: POTATO LEAF DETECTION
    # ========================================================

    with torch.no_grad():

        detector_outputs = detector_model(image_tensor)

        detector_probabilities = torch.softmax(
            detector_outputs,
            dim=1
        )

        not_potato_probability = detector_probabilities[
            0, 0
        ].item()

        potato_probability = detector_probabilities[
            0, 1
        ].item()

    # ========================================================
    # REJECT IF NOT POTATO LEAF
    # ========================================================

    if potato_probability < DETECTOR_THRESHOLD:

        return {
            "is_potato_leaf": False,
            "potato_probability": potato_probability,
            "not_potato_probability": not_potato_probability,
            "prediction": None,
            "confidence": None,
            "confidence_level": None,
            "explanation": (
                "This image does not appear to be a potato leaf, "
                "so the disease classifier was not used."
            ),
            "recommendation": (
                "Please upload a clear photo of a potato leaf. "
                "Try to make sure the leaf is clearly visible and well lit."
            )
        }

    # ========================================================
    # STEP 2: DISEASE CLASSIFICATION
    # ========================================================

    with torch.no_grad():

        outputs = disease_model(image_tensor)

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        confidence, predicted_class = torch.max(
            probabilities,
            dim=1
        )

    prediction = DISEASE_CLASS_NAMES[
        predicted_class.item()
    ]

    confidence = confidence.item()

    # ========================================================
    # GENERATE EXPLANATION AND RECOMMENDATION
    # ========================================================

    explanation_data = generate_explanation(
        prediction,
        confidence
    )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {
        "is_potato_leaf": True,
        "potato_probability": potato_probability,
        "not_potato_probability": not_potato_probability,
        "prediction": prediction,
        "confidence": confidence,
        "confidence_level": explanation_data["confidence_level"],
        "explanation": explanation_data["explanation"],
        "recommendation": explanation_data["recommendation"]
    }