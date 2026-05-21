"""
Utilidades de seguridad para autenticación y autorización.

Este archivo contiene funciones para:
- cifrar contraseñas,
- verificar contraseñas,
- crear tokens JWT,
- obtener el usuario autenticado desde el token.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.connection import get_db
from app.models.user import User


# Contexto de cifrado de contraseñas usando bcrypt.
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# URL del endpoint donde el usuario hará login.
bearer_scheme = HTTPBearer()


def hash_password(password: str) -> str:
    """
    Cifra una contraseña en texto plano.

    bcrypt tiene un límite interno de 72 bytes, por eso validamos
    la longitud antes de generar el hash.
    """
    if len(password.encode("utf-8")) > 72:
        raise ValueError("La contraseña no puede superar los 72 bytes.")

    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Comprueba si una contraseña en texto plano coincide con su hash.
    """
    if len(plain_password.encode("utf-8")) > 72:
        return False

    return password_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT firmado.

    Args:
        data (dict): Datos que se guardarán dentro del token.
        expires_delta (Optional[timedelta]): Tiempo de expiración opcional.

    Returns:
        str: Token JWT generado.
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Obtiene el usuario autenticado a partir del token JWT.

    Args:
        credentials (HTTPAuthorizationCredentials): Credenciales Bearer enviadas en la cabecera Authorization.
        db (Session): Sesión de base de datos.

    Raises:
        HTTPException: Si el token no es válido o el usuario no existe.

    Returns:
        User: Usuario autenticado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario está desactivado.",
        )

    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Comprueba que el usuario autenticado tenga rol ADMIN.

    Args:
        current_user (User): Usuario autenticado.

    Raises:
        HTTPException: Si el usuario no es administrador.

    Returns:
        User: Usuario administrador.
    """
    if current_user.role.name != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador.",
        )

    return current_user