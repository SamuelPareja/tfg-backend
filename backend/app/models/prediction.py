"""
Modelos ORM para las tablas predictions y prediction_matches.
"""

from sqlalchemy import (
    Column,
    BigInteger,
    ForeignKey,
    String,
    Text,
    DECIMAL,
    TIMESTAMP,
    text,
    Enum,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class Prediction(Base):
    """
    Representa una predicción completa generada por un usuario.
    """

    __tablename__ = "predictions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    title = Column(String(150), nullable=False, default="Predicción de quiniela")
    model_used = Column(String(80), nullable=False, default="ensemble")
    global_confidence = Column(DECIMAL(5, 2))
    ai_explanation = Column(Text)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship("User", back_populates="predictions")
    matches = relationship(
        "PredictionMatch",
        back_populates="prediction",
        cascade="all, delete-orphan",
    )
    favorites = relationship("Favorite", back_populates="prediction")
    audits = relationship("PredictionAudit", back_populates="prediction")


class PredictionMatch(Base):
    """
    Representa un partido concreto dentro de una predicción.
    """

    __tablename__ = "prediction_matches"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    prediction_id = Column(BigInteger, ForeignKey("predictions.id"), nullable=False)
    home_team = Column(String(120), nullable=False)
    away_team = Column(String(120), nullable=False)
    predicted_result = Column(Enum("1", "X", "2"), nullable=False)
    home_win_probability = Column(DECIMAL(5, 2))
    draw_probability = Column(DECIMAL(5, 2))
    away_win_probability = Column(DECIMAL(5, 2))
    confidence = Column(DECIMAL(5, 2))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    prediction = relationship("Prediction", back_populates="matches")