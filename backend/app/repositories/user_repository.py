"""
Repositorio de usuarios.

Centraliza las consultas a base de datos relacionadas con usuarios.
"""

from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Busca un usuario por email.

    Args:
        db (Session): Sesión de base de datos.
        email (str): Email del usuario.

    Returns:
        User | None: Usuario encontrado o None.
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Busca un usuario por nombre de usuario.

    Args:
        db (Session): Sesión de base de datos.
        username (str): Nombre de usuario.

    Returns:
        User | None: Usuario encontrado o None.
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Busca un usuario por ID.

    Args:
        db (Session): Sesión de base de datos.
        user_id (int): ID del usuario.

    Returns:
        User | None: Usuario encontrado o None.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_default_user_role(db: Session) -> Role:
    """
    Obtiene el rol USER por defecto.

    Args:
        db (Session): Sesión de base de datos.

    Returns:
        Role: Rol USER.
    """
    return db.query(Role).filter(Role.name == "USER").first()


def create_user(
    db: Session,
    username: str,
    email: str,
    password_hash: str,
    full_name: str | None,
    role_id: int,
) -> User:
    """
    Crea un nuevo usuario en base de datos.

    Args:
        db (Session): Sesión de base de datos.
        username (str): Nombre de usuario.
        email (str): Email del usuario.
        password_hash (str): Contraseña cifrada.
        full_name (str | None): Nombre completo.
        role_id (int): ID del rol asignado.

    Returns:
        User: Usuario creado.
    """
    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        full_name=full_name,
        role_id=role_id,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user