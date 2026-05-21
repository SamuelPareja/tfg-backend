# Importa FastAPI para crear la aplicación web
from fastapi import FastAPI

# Importa el middleware CORS para permitir comunicación con el frontend
from fastapi.middleware.cors import CORSMiddleware

# Importa las rutas de predicción
from app.routes.predict import router as predict_router

# Importa las rutas de equipos
from app.routes.teams import router as teams_router

# “Este archivo es el punto de entrada del backend. Configura FastAPI,
#  habilita CORS para comunicarse con React y registra las rutas de la aplicación.”
# “CORS permite que el frontend y el backend se comuniquen aunque estén en distintos puertos.”


# Crea la aplicación FastAPI con un título
app = FastAPI(title="Aquinielator API")

# Configura CORS (Cross-Origin Resource Sharing)
# Permite que el frontend (React) pueda comunicarse con el backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Permite peticiones desde el frontend en desarrollo
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)

# Endpoint de prueba para comprobar que la API está funcionando
@app.get("/health")
def health():
    return {"status": "ok"}

# Registra las rutas de predicción bajo el prefijo /api
app.include_router(predict_router, prefix="/api")

# Registra las rutas de equipos bajo el prefijo /api
app.include_router(teams_router, prefix="/api")