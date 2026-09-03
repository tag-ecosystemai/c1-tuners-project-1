from pathlib import Path
from tempfile import NamedTemporaryFile
from PIL import UnidentifiedImageError

from fastapi import APIRouter, File, HTTPException, UploadFile

from ai.inference.predict import predict

from backend.schemas.prediction import PredictionResponse


router = APIRouter()

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


@router.post("/predict", response_model=PredictionResponse)
async def predict_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Please upload a JPEG, PNG, or WebP image.",
        )

    suffix = Path(file.filename or "").suffix

    with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        image_path = temp_file.name
        temp_file.write(await file.read())

    try:
        result = predict(image_path)
        return result
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file could not be read as an image.",
        )
    finally:
        Path(image_path).unlink(missing_ok=True)