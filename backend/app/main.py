"""
Punto de entrada principal del backend de Aquinielator.

Este archivo crea la aplicación FastAPI, configura CORS,
registra los routers principales y define endpoints básicos
como el health check.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes.predict import router as predict_router
from app.routes.teams import router as teams_router
from app.routes.database_test import router as database_test_router
from app.routes.auth import router as auth_router
from app.routes.predictions import router as predictions_router
from app.routes.favorites import router as favorites_router


# Crea la aplicación FastAPI.
# FastAPI genera automáticamente documentación Swagger en /docs.
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="API para generar predicciones de quinielas de fútbol usando modelos clásicos, ML e IA.",
)


# Configuración CORS.
# Permite que el frontend pueda comunicarse con el backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health():
    """
    Comprueba si la API está funcionando correctamente.

    Returns:
        dict: Estado básico del backend.
    """
    return {
        "status": "ok",
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
    }


# Rutas principales de la API.
app.include_router(predict_router, prefix="/api", tags=["Predicciones"])
app.include_router(teams_router, prefix="/api", tags=["Equipos"])
app.include_router(database_test_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(predictions_router, prefix="/api")
app.include_router(favorites_router, prefix="/api")