"""
Servicio de equipos.

Contiene la lógica de negocio para consultar equipos disponibles.
"""

from sqlalchemy.orm import Session

from app.repositories.team_repository import get_all_teams_from_db
from app.schemas.team_schema import TeamResponse


def list_teams(db: Session) -> list[TeamResponse]:
    """
    Lista los equipos disponibles en la base de datos.

    Args:
        db (Session): Sesión de base de datos.

    Returns:
        list[TeamResponse]: Lista de equipos.
    """
    teams = get_all_teams_from_db(db)

    return [
        TeamResponse(
            id=team.id,
            name=team.name,
            stats_name=team.stats_name,
            csv_name=team.csv_name,
            short_name=team.short_name,
            league=team.league,
            country=team.country,
        )
        for team in teams
    ]