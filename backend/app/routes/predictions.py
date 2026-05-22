"""
Rutas para gestionar el historial de predicciones.

Estos endpoints permiten guardar, listar, consultar y eliminar
predicciones del usuario autenticado.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.prediction_history_schema import (
    PredictionCreateRequest,
    PredictionResponse,
    PredictionSummaryResponse,
)
from app.services.prediction_history_service import (
    delete_user_prediction,
    get_user_prediction,
    list_user_predictions,
    save_prediction,
)


router = APIRouter(prefix="/predictions", tags=["Historial de predicciones"])


def build_prediction_summary_response(prediction) -> PredictionSummaryResponse:
    """
    Convierte una predicción en una respuesta resumida.

    Args:
        prediction: Predicción de SQLAlchemy.

    Returns:
        PredictionSummaryResponse: Resumen de la predicción.
    """
    return PredictionSummaryResponse(
        id=prediction.id,
        title=prediction.title,
        model_used=prediction.model_used,
        global_confidence=prediction.global_confidence,
        created_at=prediction.created_at,
        total_matches=len(prediction.matches),
    )


@router.post(
    "",
    response_model=PredictionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_prediction_endpoint(
    prediction_data: PredictionCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Guarda una predicción en el historial del usuario autenticado.

    Returns:
        PredictionResponse: Predicción guardada.
    """
    return save_prediction(
        db=db,
        user_id=current_user.id,
        prediction_data=prediction_data,
    )


@router.get("/me", response_model=list[PredictionSummaryResponse])
def get_my_predictions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Lista todas las predicciones del usuario autenticado.

    Returns:
        list[PredictionSummaryResponse]: Historial del usuario.
    """
    predictions = list_user_predictions(db, current_user.id)

    return [
        build_prediction_summary_response(prediction)
        for prediction in predictions
    ]


@router.get("/{prediction_id}", response_model=PredictionResponse)
def get_prediction_detail(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Obtiene el detalle de una predicción concreta.

    Returns:
        PredictionResponse: Predicción con sus partidos.
    """
    return get_user_prediction(
        db=db,
        user_id=current_user.id,
        prediction_id=prediction_id,
    )


@router.delete("/{prediction_id}")
def delete_prediction_endpoint(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Elimina una predicción del historial del usuario autenticado.

    Returns:
        dict: Mensaje de confirmación.
    """
    return delete_user_prediction(
        db=db,
        user_id=current_user.id,
        prediction_id=prediction_id,
    )