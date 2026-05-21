# Importa APIRouter para crear rutas independientes en FastAPI
from fastapi import APIRouter

# Importa la función que devuelve la lista de equipos
from app.services.data_service import get_all_teams

# Crea un router para agrupar endpoints relacionados
router = APIRouter()

# “Este endpoint devuelve la lista de equipos desde el backend
#  para que el frontend pueda rellenar los desplegables.”

# Endpoint GET /teams
@router.get("/teams")
def list_teams():
    # Devuelve un JSON con la lista de equipos
    return {"equipos": get_all_teams()}