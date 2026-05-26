"""
Rutas relacionadas con usuarios.

Incluye endpoints protegidos para obtener información adicional
del usuario autenticado.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.user_stats_schema import UserStatsResponse
from app.services.user_stats_service import get_user_stats


router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.get("/me/stats", response_model=UserStatsResponse)
def get_my_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Devuelve estadísticas básicas del usuario autenticado.

    Returns:
        UserStatsResponse: Total de predicciones, favoritos y última predicción.
    """
    return get_user_stats(db=db, user_id=current_user.id)