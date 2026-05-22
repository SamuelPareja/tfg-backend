"""
Schemas relacionados con equipos.

Estos modelos definen cómo se devuelven los equipos desde la API.
"""

from pydantic import BaseModel


class TeamResponse(BaseModel):
    """
    Respuesta pública de un equipo.
    """

    id: int
    name: str
    stats_name: str
    csv_name: str
    short_name: str | None
    league: str | None
    country: str | None

    class Config:
        from_attributes = True