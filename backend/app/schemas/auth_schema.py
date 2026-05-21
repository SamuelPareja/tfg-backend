"""
Schemas de autenticación.

Estos modelos Pydantic validan los datos recibidos y enviados
en los endpoints de registro, login y usuario autenticado.
"""

from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    """
    Datos necesarios para registrar un usuario.
    """

    username: str = Field(..., min_length=3, max_length=80)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    full_name: str | None = Field(default=None, max_length=120)


class UserLoginRequest(BaseModel):
    """
    Datos necesarios para iniciar sesión.
    """

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """
    Respuesta devuelta después de un login correcto.
    """

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """
    Datos públicos de un usuario.
    """

    id: int
    username: str
    email: EmailStr
    full_name: str | None
    role: str
    is_active: bool

    class Config:
        from_attributes = True