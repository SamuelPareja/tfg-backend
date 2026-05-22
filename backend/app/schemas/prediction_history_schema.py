"""
Schemas para guardar y consultar predicciones en MySQL.

Estos modelos Pydantic validan los datos de entrada y salida
relacionados con el historial de predicciones del usuario.
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class PredictionMatchCreate(BaseModel):
    """
    Datos necesarios para guardar un partido dentro de una predicción.
    """

    home_team: str = Field(..., min_length=1, max_length=120)
    away_team: str = Field(..., min_length=1, max_length=120)
    predicted_result: str = Field(..., pattern="^(1|X|2)$")
    home_win_probability: float | None = Field(default=None, ge=0, le=100)
    draw_probability: float | None = Field(default=None, ge=0, le=100)
    away_win_probability: float | None = Field(default=None, ge=0, le=100)
    confidence: float | None = Field(default=None, ge=0, le=100)


class PredictionCreateRequest(BaseModel):
    """
    Datos necesarios para guardar una predicción completa.
    """

    title: str = Field(default="Predicción de quiniela", max_length=150)
    model_used: str = Field(default="ensemble", max_length=80)
    global_confidence: float | None = Field(default=None, ge=0, le=100)
    ai_explanation: str | None = None
    matches: list[PredictionMatchCreate] = Field(..., min_length=1)


class PredictionMatchResponse(BaseModel):
    """
    Datos devueltos de un partido guardado.
    """

    id: int
    home_team: str
    away_team: str
    predicted_result: str
    home_win_probability: Decimal | None
    draw_probability: Decimal | None
    away_win_probability: Decimal | None
    confidence: Decimal | None
    created_at: datetime

    class Config:
        from_attributes = True


class PredictionResponse(BaseModel):
    """
    Datos devueltos de una predicción guardada.
    """

    id: int
    title: str
    model_used: str
    global_confidence: Decimal | None
    ai_explanation: str | None
    created_at: datetime
    updated_at: datetime
    matches: list[PredictionMatchResponse]

    class Config:
        from_attributes = True


class PredictionSummaryResponse(BaseModel):
    """
    Resumen de una predicción para listados.
    """

    id: int
    title: str
    model_used: str
    global_confidence: Decimal | None
    created_at: datetime
    total_matches: int

    class Config:
        from_attributes = True