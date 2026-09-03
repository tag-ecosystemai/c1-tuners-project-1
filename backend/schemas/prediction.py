from typing import Optional

from pydantic import BaseModel


class PredictionResponse(BaseModel):
    is_potato_leaf: bool
    potato_probability: float
    not_potato_probability: float
    prediction: Optional[str] = None
    confidence: Optional[float] = None
    confidence_level: Optional[str] = None
    explanation: Optional[str] = None
    recommendation: Optional[str] = None