"""
Base declarativa de SQLAlchemy.

Todos los modelos ORM de la aplicación heredan de esta clase Base.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()