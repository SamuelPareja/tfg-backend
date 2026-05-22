"""
Servicio de historial de predicciones.

Contiene la lógica de negocio relacionada con guardar,
listar, consultar y eliminar predicciones del usuario.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.prediction import Prediction
from app.repositories.prediction_repository import (
    create_prediction,
    delete_prediction_by_id_and_user,
    get_prediction_by_id_and_user,
    get_predictions_by_user,
)
from app.schemas.prediction_history_schema import PredictionCreateRequest


def save_prediction(
    db: Session,
    user_id: int,
    prediction_data: PredictionCreateRequest,
) -> Prediction:
    """
    Guarda una predicción para el usuario autenticado.

    Args:
        db (Session): Sesión de base de datos.
        user_id (int): ID del usuario autenticado.
        prediction_data (PredictionCreateRequest): Datos de la predicción.

    Returns:
        Prediction: Predicción guardada.
    """
    return create_prediction(db, user_id, prediction_data)


def list_user_predictions(db: Session, user_id: int) -> list[Prediction]:
    """
    Lista todas las predicciones de un usuario.

    Args:
        db (Session): Sesión de base de datos.
        user_id (int): ID del usuario autenticado.

    Returns:
        list[Prediction]: Predicciones del usuario.
    """
    return get_predictions_by_user(db, user_id)


def get_user_prediction(
    db: Session,
    user_id: int,
    prediction_id: int,
) -> Prediction:
    """
    Obtiene una predicción concreta de un usuario.

    Raises:
        HTTPException: Si la predicción no existe.

    Returns:
        Prediction: Predicción encontrada.
    """
    prediction = get_prediction_by_id_and_user(db, prediction_id, user_id)

    if prediction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Predicción no encontrada.",
        )

    return prediction


def delete_user_prediction(
    db: Session,
    user_id: int,
    prediction_id: int,
) -> dict:
    """
    Elimina una predicción de un usuario.

    Raises:
        HTTPException: Si la predicción no existe.

    Returns:
        dict: Mensaje de confirmación.
    """
    deleted = delete_prediction_by_id_and_user(db, prediction_id, user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Predicción no encontrada.",
        )

    return {"message": "Predicción eliminada correctamente."}