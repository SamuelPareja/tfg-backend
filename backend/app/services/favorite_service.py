"""
Servicio de favoritos.

Contiene la lógica de negocio para marcar, listar y eliminar
predicciones favoritas del usuario.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.favorite import Favorite
from app.repositories.favorite_repository import (
    create_favorite,
    delete_favorite,
    get_favorite_by_user_and_prediction,
    get_favorites_by_user,
    get_prediction_by_id_and_user,
)


def add_prediction_to_favorites(
    db: Session,
    user_id: int,
    prediction_id: int,
) -> Favorite:
    """
    Marca una predicción como favorita.

    Raises:
        HTTPException: Si la predicción no existe o ya está en favoritos.

    Returns:
        Favorite: Favorito creado.
    """
    prediction = get_prediction_by_id_and_user(
        db=db,
        prediction_id=prediction_id,
        user_id=user_id,
    )

    if prediction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Predicción no encontrada.",
        )

    existing_favorite = get_favorite_by_user_and_prediction(
        db=db,
        user_id=user_id,
        prediction_id=prediction_id,
    )

    if existing_favorite:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La predicción ya está marcada como favorita.",
        )

    return create_favorite(
        db=db,
        user_id=user_id,
        prediction_id=prediction_id,
    )


def list_user_favorites(db: Session, user_id: int) -> list[Favorite]:
    """
    Lista las predicciones favoritas de un usuario.

    Args:
        db (Session): Sesión de base de datos.
        user_id (int): ID del usuario.

    Returns:
        list[Favorite]: Lista de favoritos.
    """
    return get_favorites_by_user(db, user_id)


def remove_prediction_from_favorites(
    db: Session,
    user_id: int,
    prediction_id: int,
) -> dict:
    """
    Quita una predicción de favoritos.

    Raises:
        HTTPException: Si la predicción no estaba en favoritos.

    Returns:
        dict: Mensaje de confirmación.
    """
    deleted = delete_favorite(
        db=db,
        user_id=user_id,
        prediction_id=prediction_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La predicción no estaba marcada como favorita.",
        )

    return {"message": "Predicción eliminada de favoritos correctamente."}