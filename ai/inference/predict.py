import torch
from PIL import Image

from ai.models.model import create_model
from ai.data.preprocessing import val_test_transform


MODEL_PATH = "ai/models/weights/potato_resnet18_best.pth"

CLASS_NAMES = [
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy"
]


# DEVICE

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# LOAD MODEL ONCE

model = create_model()

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=device
    )
)

model = model.to(device)

model.eval()


# PREDICT

def predict(image_path):

    image = Image.open(image_path).convert("RGB")

    image = val_test_transform(image)

    image = image.unsqueeze(0)

    image = image.to(device)

    with torch.no_grad():

        outputs = model(image)

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        confidence, predicted_class = torch.max(
            probabilities,
            dim=1
        )

    prediction = CLASS_NAMES[
        predicted_class.item()
    ]

    confidence = confidence.item()

    return {
        "prediction": prediction,
        "confidence": confidence
    }