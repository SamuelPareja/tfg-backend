"""
Repositorio de estadísticas de usuario.

Centraliza las consultas a base de datos necesarias para calcular
el resumen de actividad del usuario autenticado.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.favorite import Favorite
from app.models.prediction import Prediction


def count_user_predictions(db: Session, user_id: int) -> int:
    """
    Cuenta cuántas predicciones tiene guardadas un usuario.

    Args:
        db (Session): Sesión de base de datos.
        user_id (int): ID del usuario.

    Returns:
        int: Número total de predicciones.
    """
    return (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .count()
    )


def count_user_favorites(db: Session, user_id: int) -> int:
    """
    Cuenta cuántas predicciones favoritas tiene un usuario.

    Args:
        db (Session): Sesión de base de datos.
        user_id (int): ID del usuario.

    Returns:
        int: Número total de favoritos.
    """
    return (
        db.query(Favorite)
        .filter(Favorite.user_id == user_id)
        .count()
    )


def get_last_prediction_date(db: Session, user_id: int) -> datetime | None:
    """
    Obtiene la fecha de la última predicción guardada por el usuario.

    Args:
        db (Session): Sesión de base de datos.
        user_id (int): ID del usuario.

    Returns:
        datetime | None: Fecha de última predicción o None.
    """
    last_prediction = (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .first()
    )

    if last_prediction is None:
        return None

    return last_prediction.created_at