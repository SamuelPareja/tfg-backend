"""
Configuración de conexión entre FastAPI y MySQL.

Este archivo crea el motor de SQLAlchemy, la sesión de base de datos
y una dependencia reutilizable para usar la BBDD en los endpoints.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# Motor principal de SQLAlchemy.
# pool_pre_ping=True evita errores si MySQL cierra conexiones inactivas.
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

# Crea sesiones de base de datos.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    Dependencia de FastAPI para obtener una sesión de base de datos.

    Abre una sesión, la entrega al endpoint y la cierra automáticamente
    al terminar la petición.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()