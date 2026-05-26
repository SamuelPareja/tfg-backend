"""
Servicio de estadísticas de usuario.

Contiene la lógica para construir el resumen de actividad
del usuario autenticado.
"""

from sqlalchemy.orm import Session

from app.repositories.user_stats_repository import (
    count_user_favorites,
    count_user_predictions,
    get_last_prediction_date,
)
from app.schemas.user_stats_schema import UserStatsResponse


def get_user_stats(db: Session, user_id: int) -> UserStatsResponse:
    """
    Devuelve estadísticas básicas del usuario autenticado.

    Args:
        db (Session): Sesión de base de datos.
        user_id (int): ID del usuario.

    Returns:
        UserStatsResponse: Resumen de actividad del usuario.
    """
    return UserStatsResponse(
        total_predictions=count_user_predictions(db, user_id),
        total_favorites=count_user_favorites(db, user_id),
        last_prediction_date=get_last_prediction_date(db, user_id),
    )