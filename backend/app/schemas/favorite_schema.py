"""
Schemas para favoritos.

Estos modelos Pydantic definen las respuestas relacionadas con
predicciones marcadas como favoritas por el usuario.
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class FavoritePredictionResponse(BaseModel):
    """
    Datos de una predicción marcada como favorita.
    """

    favorite_id: int
    prediction_id: int
    title: str
    model_used: str
    global_confidence: Decimal | None
    created_at: datetime
    favorite_created_at: datetime
    total_matches: int

    class Config:
        from_attributes = True