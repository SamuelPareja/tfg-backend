"""
Repositorio de predicciones.

Centraliza las consultas a base de datos relacionadas con
predicciones y partidos predichos.
"""

from sqlalchemy.orm import Session, joinedload

from app.models.prediction import Prediction, PredictionMatch
from app.schemas.prediction_history_schema import PredictionCreateRequest


def create_prediction(
    db: Session,
    user_id: int,
    prediction_data: PredictionCreateRequest,
) -> Prediction:
    """
    Guarda una predicción completa en la base de datos.

    Args:
        db (Session): Sesión de base de datos.
        user_id (int): ID del usuario autenticado.
        prediction_data (PredictionCreateRequest): Datos de la predicción.

    Returns:
        Prediction: Predicción creada.
    """
    prediction = Prediction(
        user_id=user_id,
        title=prediction_data.title,
        model_used=prediction_data.model_used,
        global_confidence=prediction_data.global_confidence,
        ai_explanation=prediction_data.ai_explanation,
    )

    db.add(prediction)
    db.flush()

    for match_data in prediction_data.matches:
        match = PredictionMatch(
            prediction_id=prediction.id,
            home_team=match_data.home_team,
            away_team=match_data.away_team,
            predicted_result=match_data.predicted_result,
            home_win_probability=match_data.home_win_probability,
            draw_probability=match_data.draw_probability,
            away_win_probability=match_data.away_win_probability,
            confidence=match_data.confidence,
        )

        db.add(match)

    db.commit()
    db.refresh(prediction)

    return get_prediction_by_id_and_user(db, prediction.id, user_id)


def get_predictions_by_user(db: Session, user_id: int) -> list[Prediction]:
    """
    Obtiene todas las predicciones de un usuario.

    Args:
        db (Session): Sesión de base de datos.
        user_id (int): ID del usuario.

    Returns:
        list[Prediction]: Lista de predicciones.
    """
    return (
        db.query(Prediction)
        .options(joinedload(Prediction.matches))
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .all()
    )


def get_prediction_by_id_and_user(
    db: Session,
    prediction_id: int,
    user_id: int,
) -> Prediction | None:
    """
    Obtiene una predicción concreta de un usuario.

    Args:
        db (Session): Sesión de base de datos.
        prediction_id (int): ID de la predicción.
        user_id (int): ID del usuario.

    Returns:
        Prediction | None: Predicción encontrada o None.
    """
    return (
        db.query(Prediction)
        .options(joinedload(Prediction.matches))
        .filter(
            Prediction.id == prediction_id,
            Prediction.user_id == user_id,
        )
        .first()
    )


def delete_prediction_by_id_and_user(
    db: Session,
    prediction_id: int,
    user_id: int,
) -> bool:
    """
    Elimina una predicción concreta de un usuario.

    Args:
        db (Session): Sesión de base de datos.
        prediction_id (int): ID de la predicción.
        user_id (int): ID del usuario.

    Returns:
        bool: True si se elimina, False si no existe.
    """
    prediction = get_prediction_by_id_and_user(db, prediction_id, user_id)

    if prediction is None:
        return False

    db.delete(prediction)
    db.commit()

    return True