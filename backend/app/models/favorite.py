"""
Modelo ORM para la tabla favorites.
"""

from sqlalchemy import Column, BigInteger, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship

from app.database.base import Base


class Favorite(Base):
    """
    Representa una predicción marcada como favorita por un usuario.
    """

    __tablename__ = "favorites"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    prediction_id = Column(BigInteger, ForeignKey("predictions.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship("User", back_populates="favorites")
    prediction = relationship("Prediction", back_populates="favorites")