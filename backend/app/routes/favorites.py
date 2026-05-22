"""
Rutas para gestionar predicciones favoritas.

Estos endpoints permiten marcar, listar y eliminar favoritos
del usuario autenticado.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.favorite_schema import FavoritePredictionResponse
from app.services.favorite_service import (
    add_prediction_to_favorites,
    list_user_favorites,
    remove_prediction_from_favorites,
)


router = APIRouter(prefix="/favorites", tags=["Favoritos"])


def build_favorite_response(favorite) -> FavoritePredictionResponse:
    """
    Convierte un favorito de SQLAlchemy en respuesta para la API.

    Args:
        favorite: Registro favorito de SQLAlchemy.

    Returns:
        FavoritePredictionResponse: Datos de la predicción favorita.
    """
    prediction = favorite.prediction

    return FavoritePredictionResponse(
        favorite_id=favorite.id,
        prediction_id=prediction.id,
        title=prediction.title,
        model_used=prediction.model_used,
        global_confidence=prediction.global_confidence,
        created_at=prediction.created_at,
        favorite_created_at=favorite.created_at,
        total_matches=len(prediction.matches),
    )


@router.post(
    "/{prediction_id}",
    response_model=FavoritePredictionResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_favorite_endpoint(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Marca una predicción del usuario autenticado como favorita.

    Returns:
        FavoritePredictionResponse: Predicción marcada como favorita.
    """
    favorite = add_prediction_to_favorites(
        db=db,
        user_id=current_user.id,
        prediction_id=prediction_id,
    )

    return build_favorite_response(favorite)


@router.get("/me", response_model=list[FavoritePredictionResponse])
def get_my_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Lista todas las predicciones favoritas del usuario autenticado.

    Returns:
        list[FavoritePredictionResponse]: Favoritos del usuario.
    """
    favorites = list_user_favorites(db, current_user.id)

    return [
        build_favorite_response(favorite)
        for favorite in favorites
    ]


@router.delete("/{prediction_id}")
def delete_favorite_endpoint(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Elimina una predicción de favoritos del usuario autenticado.

    Returns:
        dict: Mensaje de confirmación.
    """
    return remove_prediction_from_favorites(
        db=db,
        user_id=current_user.id,
        prediction_id=prediction_id,
    )