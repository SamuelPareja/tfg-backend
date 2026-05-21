"""
Servicio de autenticación.

Contiene la lógica de negocio para registrar usuarios,
iniciar sesión y generar tokens JWT.
"""

from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import (
    create_user,
    get_default_user_role,
    get_user_by_email,
    get_user_by_username,
)
from app.schemas.auth_schema import UserRegisterRequest


def register_user(db: Session, user_data: UserRegisterRequest) -> User:
    """
    Registra un nuevo usuario en la aplicación.

    Args:
        db (Session): Sesión de base de datos.
        user_data (UserRegisterRequest): Datos recibidos del formulario.

    Raises:
        HTTPException: Si el email o username ya existen.

    Returns:
        User: Usuario creado.
    """
    existing_email = get_user_by_email(db, user_data.email)

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario registrado con ese email.",
        )

    existing_username = get_user_by_username(db, user_data.username)

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario registrado con ese nombre de usuario.",
        )

    default_role = get_default_user_role(db)

    if default_role is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No existe el rol USER en la base de datos.",
        )

    password_hash = hash_password(user_data.password)

    return create_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password_hash=password_hash,
        full_name=user_data.full_name,
        role_id=default_role.id,
    )


def authenticate_user(db: Session, email: str, password: str) -> User:
    """
    Autentica un usuario por email y contraseña.

    Args:
        db (Session): Sesión de base de datos.
        email (str): Email introducido.
        password (str): Contraseña introducida.

    Raises:
        HTTPException: Si las credenciales son incorrectas.

    Returns:
        User: Usuario autenticado.
    """
    user = get_user_by_email(db, email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos.",
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario está desactivado.",
        )

    return user


def create_user_token(user: User) -> str:
    """
    Genera un token JWT para un usuario autenticado.

    Args:
        user (User): Usuario autenticado.

    Returns:
        str: Token JWT.
    """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.name,
        },
        expires_delta=access_token_expires,
    )

    return token