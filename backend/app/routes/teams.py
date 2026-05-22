"""
Rutas relacionadas con equipos.

Este endpoint devuelve los equipos desde MySQL para que el frontend
pueda rellenar desplegables y trabajar con nombres consistentes.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.team_service import list_teams


router = APIRouter()


@router.get("/teams")
def get_teams(db: Session = Depends(get_db)):
    """
    Devuelve los equipos disponibles.

    Returns:
        dict: Lista simple de nombres y lista detallada de equipos.
    """
    teams = list_teams(db)

    return {
        "equipos": [team.name for team in teams],
        "equipos_detalle": teams,
    }