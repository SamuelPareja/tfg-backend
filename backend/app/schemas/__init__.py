"""
Schemas generales de la aplicación.

Este archivo reexporta los schemas principales para mantener compatibilidad
con imports antiguos como: from app.schemas import QuinielaRequest.
"""

from app.schemas.prediction_schema import (
    QuinielaRequest,
    QuinielaResponse,
    MatchPrediction,
)