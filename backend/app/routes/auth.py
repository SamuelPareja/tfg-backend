"""
Rutas de autenticación.

Contiene los endpoints de registro, inicio de sesión
y obtención del usuario autenticado.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.schemas.auth_schema import (
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.services.auth_service import (
    authenticate_user,
    create_user_token,
    register_user,
)


router = APIRouter(prefix="/auth", tags=["Autenticación"])


def build_user_response(user: User) -> UserResponse:
    """
    Convierte un modelo User de SQLAlchemy en un UserResponse.

    Args:
        user (User): Usuario de base de datos.

    Returns:
        UserResponse: Datos públicos del usuario.
    """
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role.name,
        is_active=user.is_active,
    )


@router.post("/register", response_model=UserResponse)
def register(
    user_data: UserRegisterRequest,
    db: Session = Depends(get_db),
):
    """
    Registra un usuario nuevo en Aquinielator.

    Returns:
        UserResponse: Usuario registrado sin mostrar la contraseña.
    """
    user = register_user(db, user_data)
    return build_user_response(user)


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: UserLoginRequest,
    db: Session = Depends(get_db),
):
    """
    Inicia sesión con email y contraseña.

    Returns:
        TokenResponse: Token JWT para usar en endpoints protegidos.
    """
    user = authenticate_user(db, login_data.email, login_data.password)
    access_token = create_user_token(user)

    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Devuelve los datos del usuario autenticado.

    Returns:
        UserResponse: Datos públicos del usuario actual.
    """
    return build_user_response(current_user)