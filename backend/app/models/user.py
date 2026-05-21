"""
Modelo ORM para la tabla users.
"""

from sqlalchemy import Boolean, Column, BigInteger, ForeignKey, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

from app.database.base import Base


class User(Base):
    """
    Representa un usuario registrado en Aquinielator.
    """

    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(80), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(120))
    is_active = Column(Boolean, nullable=False, default=True)
    role_id = Column(BigInteger, ForeignKey("roles.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    role = relationship("Role", back_populates="users")
    predictions = relationship("Prediction", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")
    login_audits = relationship("LoginAudit", back_populates="user")
    prediction_audits = relationship("PredictionAudit", back_populates="user")