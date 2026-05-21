"""
Modelo ORM para la tabla teams.
"""

from sqlalchemy import Column, BigInteger, String, TIMESTAMP, text

from app.database.base import Base


class Team(Base):
    """
    Representa un equipo de fútbol disponible para las predicciones.

    name: nombre mostrado en frontend.
    stats_name: nombre usado en teams_stats.json.
    csv_name: nombre usado en los CSV históricos.
    """

    __tablename__ = "teams"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False, unique=True)
    stats_name = Column(String(120), nullable=False)
    csv_name = Column(String(120), nullable=False)
    short_name = Column(String(20))
    league = Column(String(100), default="LaLiga")
    country = Column(String(100), default="España")
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))