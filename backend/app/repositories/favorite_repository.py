"""
Repositorio de favoritos.

Centraliza las consultas a base de datos relacionadas con favoritos.
"""

from sqlalchemy.orm import Session, joinedload

from app.models.favorite import Favorite
from app.models.prediction import Prediction


def get_favorite_by_user_and_prediction(
    db: Session,
    user_id: int,
    prediction_id: int,
) -> Favorite | None:
    """
    Busca si una predicción ya está marcada como favorita por un usuario.

    Args:
        db (Session): Sesión de base de datos.
        user_id (int): ID del usuario.
        prediction_id (int): ID de la predicción.

    Returns:
        Favorite | None: Favorito encontrado o None.
    """
    return (
        db.query(Favorite)
        .filter(
            Favorite.user_id == user_id,
            Favorite.prediction_id == prediction_id,
        )
        .first()
    )


def get_prediction_by_id_and_user(
    db: Session,
    prediction_id: int,
    user_id: int,
) -> Prediction | None:
    """
    Comprueba que la predicción existe y pertenece al usuario.

    Args:
        db (Session): Sesión de base de datos.
        prediction_id (int): ID de la predicción.
        user_id (int): ID del usuario.

    Returns:
        Prediction | None: Predicción encontrada o None.
    """
    return (
        db.query(Prediction)
        .filter(
            Prediction.id == prediction_id,
            Prediction.user_id == user_id,
        )
        .first()
    )


def create_favorite(
    db: Session,
    user_id: int,
    prediction_id: int,
) -> Favorite:
    """
    Marca una predicción como favorita.

    Args:
        db (Session): Sesión de base de datos.
        user_id (int): ID del usuario.
        prediction_id (int): ID de la predicción.

    Returns:
        Favorite: Favorito creado.
    """
    favorite = Favorite(
        user_id=user_id,
        prediction_id=prediction_id,
    )

    db.add(favorite)
    db.commit()
    db.refresh(favorite)

    return favorite


def get_favorites_by_user(db: Session, user_id: int) -> list[Favorite]:
    """
    Lista las predicciones favoritas de un usuario.

    Args:
        db (Session): Sesión de base de datos.
        user_id (int): ID del usuario.

    Returns:
        list[Favorite]: Lista de favoritos.
    """
    return (
        db.query(Favorite)
        .options(
            joinedload(Favorite.prediction).joinedload(Prediction.matches)
        )
        .filter(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .all()
    )


def delete_favorite(
    db: Session,
    user_id: int,
    prediction_id: int,
) -> bool:
    """
    Elimina una predicción de favoritos.

    Args:
        db (Session): Sesión de base de datos.
        user_id (int): ID del usuario.
        prediction_id (int): ID de la predicción.

    Returns:
        bool: True si se eliminó, False si no existía.
    """
    favorite = get_favorite_by_user_and_prediction(
        db=db,
        user_id=user_id,
        prediction_id=prediction_id,
    )

    if favorite is None:
        return False

    db.delete(favorite)
    db.commit()

    return True