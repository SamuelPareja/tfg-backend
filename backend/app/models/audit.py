"""
Modelos ORM para tablas de auditoría.
"""

from sqlalchemy import Boolean, Column, BigInteger, ForeignKey, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

from app.database.base import Base


class LoginAudit(Base):
    """
    Guarda intentos de inicio de sesión.
    """

    __tablename__ = "login_audit"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    email = Column(String(120), nullable=False)
    success = Column(Boolean, nullable=False)
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship("User", back_populates="login_audits")


class PredictionAudit(Base):
    """
    Guarda acciones de auditoría sobre predicciones.
    """

    __tablename__ = "prediction_audit"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    prediction_id = Column(BigInteger, ForeignKey("predictions.id"), nullable=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    action = Column(String(50), nullable=False)
    description = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship("User", back_populates="prediction_audits")
    prediction = relationship("Prediction", back_populates="audits")