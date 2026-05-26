"""
Schemas para estadísticas básicas del usuario.

Estos modelos definen la respuesta del endpoint que muestra
resumen de actividad del usuario autenticado.
"""

from datetime import datetime

from pydantic import BaseModel


class UserStatsResponse(BaseModel):
    """
    Estadísticas básicas del usuario autenticado.
    """

    total_predictions: int
    total_favorites: int
    last_prediction_date: datetime | None