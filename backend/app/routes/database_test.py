"""
Endpoints temporales para comprobar la conexión con la base de datos.

Estos endpoints sirven durante el desarrollo para verificar que FastAPI
puede leer correctamente datos desde MySQL.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.team import Team
from app.models.role import Role


router = APIRouter(prefix="/db-test", tags=["Database Test"])


@router.get("/teams")
def get_teams_from_database(db: Session = Depends(get_db)):
    """
    Obtiene todos los equipos guardados en MySQL.

    Returns:
        list: Lista de equipos registrados en la tabla teams.
    """
    teams = db.query(Team).order_by(Team.id).all()

    return [
        {
            "id": team.id,
            "name": team.name,
            "stats_name": team.stats_name,
            "csv_name": team.csv_name,
            "short_name": team.short_name,
            "league": team.league,
            "country": team.country,
        }
        for team in teams
    ]


@router.get("/roles")
def get_roles_from_database(db: Session = Depends(get_db)):
    """
    Obtiene todos los roles guardados en MySQL.

    Returns:
        list: Lista de roles disponibles en la aplicación.
    """
    roles = db.query(Role).order_by(Role.id).all()

    return [
        {
            "id": role.id,
            "name": role.name,
            "description": role.description,
        }
        for role in roles
    ]