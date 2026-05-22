"""
Endpoint informativo de la API.

Sirve para mostrar un resumen rápido de las funcionalidades disponibles
en el backend de Aquinielator.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/info", tags=["Información"])


@router.get("")
def get_api_info():
    """
    Devuelve información general del backend.

    Returns:
        dict: Resumen de funcionalidades y tecnologías.
    """
    return {
        "project": "Aquinielator API",
        "version": "1.0.0",
        "framework": "FastAPI",
        "database": "MySQL",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
        },
        "features": [
            "Registro de usuarios",
            "Login con JWT",
            "Contraseñas cifradas",
            "Roles de usuario",
            "Consulta de equipos desde MySQL",
            "Predicciones de quiniela",
            "Historial de predicciones",
            "Favoritos",
            "Auditoría con triggers",
            "Documentación Swagger",
        ],
        "main_endpoints": {
            "health": "/health",
            "teams": "/api/teams",
            "predict": "/api/predict",
            "auth": [
                "/api/auth/register",
                "/api/auth/login",
                "/api/auth/me",
            ],
            "predictions": [
                "/api/predictions",
                "/api/predictions/me",
                "/api/predictions/{prediction_id}",
            ],
            "favorites": [
                "/api/favorites/{prediction_id}",
                "/api/favorites/me",
            ],
        },
    }