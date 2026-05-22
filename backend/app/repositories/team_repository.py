"""
Repositorio de equipos.

Centraliza las consultas a base de datos relacionadas con equipos.
"""

from sqlalchemy.orm import Session

from app.models.team import Team


def get_all_teams_from_db(db: Session) -> list[Team]:
    """
    Obtiene todos los equipos guardados en MySQL.

    Args:
        db (Session): Sesión de base de datos.

    Returns:
        list[Team]: Lista de equipos ordenados por nombre.
    """
    return db.query(Team).order_by(Team.name.asc()).all()


def get_team_by_name(db: Session, team_name: str) -> Team | None:
    """
    Busca un equipo por cualquiera de sus nombres principales.

    Comprueba:
    - name
    - stats_name
    - csv_name

    Args:
        db (Session): Sesión de base de datos.
        team_name (str): Nombre del equipo.

    Returns:
        Team | None: Equipo encontrado o None.
    """
    clean_name = team_name.strip()

    return (
        db.query(Team)
        .filter(
            (Team.name == clean_name)
            | (Team.stats_name == clean_name)
            | (Team.csv_name == clean_name)
        )
        .first()
    )