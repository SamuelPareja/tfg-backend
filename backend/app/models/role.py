"""
Modelo ORM para la tabla roles.
"""

from sqlalchemy import Column, BigInteger, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

from app.database.base import Base


class Role(Base):
    """
    Representa un rol de usuario dentro de la aplicación.
    Ejemplos: USER, ADMIN.
    """

    __tablename__ = "roles"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    users = relationship("User", back_populates="role")