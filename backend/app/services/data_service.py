# Importa json para leer el archivo JSON con estadísticas
import json

# Importa Path para construir rutas de archivo de forma segura
from pathlib import Path


# Ruta al archivo JSON donde se guardan las estadísticas de los equipos
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "teams_stats.json"

# “Este servicio se encarga de cargar los datos desde un archivo JSON y preparar 
# la información necesaria para cada partido.”

# “También incluye un sistema de alias para normalizar nombres de equipos y 
# evitar errores de escritura.”

# Diccionario de alias para normalizar nombres de equipos.
# Permite aceptar nombres comunes y convertirlos a su nombre oficial.
TEAM_ALIASES = {
    # Real Madrid
    "Real Madrid": "Real Madrid",
    "Madrid": "Real Madrid",

    # Barcelona
    "FC Barcelona": "FC Barcelona",
    "Barcelona": "FC Barcelona",
    "Barça": "FC Barcelona",
    "Barca": "FC Barcelona",

    # Atlético de Madrid
    "Atlético de Madrid": "Atlético de Madrid",
    "Atletico de Madrid": "Atlético de Madrid",
    "Atlético": "Atlético de Madrid",
    "Atletico": "Atlético de Madrid",
    "Atleti": "Atlético de Madrid",
    "Ath Madrid": "Atlético de Madrid",

    # Sevilla
    "Sevilla": "Sevilla FC",
    "Sevilla FC": "Sevilla FC",

    # Betis
    "Betis": "Real Betis",
    "Real Betis": "Real Betis",

    # Real Sociedad
    "Real Sociedad": "Real Sociedad",
    "Sociedad": "Real Sociedad",

    # Villarreal
    "Villarreal": "Villarreal CF",
    "Villarreal CF": "Villarreal CF",

    # Athletic
    "Athletic Club": "Athletic Club",
    "Athletic": "Athletic Club",
    "Athletic Bilbao": "Athletic Club",
    "Ath Bilbao": "Athletic Club",

    # Valencia
    "Valencia": "Valencia CF",
    "Valencia CF": "Valencia CF",

    # Osasuna
    "Osasuna": "CA Osasuna",
    "CA Osasuna": "CA Osasuna",

    # Celta
    "Celta": "Celta",
    "Celta de Vigo": "Celta",

    # Rayo
    "Rayo Vallecano": "Rayo Vallecano",
    "Rayo": "Rayo Vallecano",
    "Vallecano": "Rayo Vallecano",

    # Alavés
    "Alavés": "Deportivo Alavés",
    "Alaves": "Deportivo Alavés",
    "Deportivo Alavés": "Deportivo Alavés",
    "Deportivo Alaves": "Deportivo Alavés",

    # Espanyol
    "RCD Espanyol": "RCD Espanyol de Barcelona",
    "Espanyol": "RCD Espanyol de Barcelona",
    "Espanol": "RCD Espanyol de Barcelona",
    "RCD Espanyol de Barcelona": "RCD Espanyol de Barcelona",

    # Elche
    "Elche": "Elche CF",
    "Elche CF": "Elche CF",

    # Getafe
    "Getafe": "Getafe CF",
    "Getafe CF": "Getafe CF",

    # Mallorca
    "Mallorca": "RCD Mallorca",
    "RCD Mallorca": "RCD Mallorca",

    # Levante
    "Levante": "Levante UD",
    "Levante UD": "Levante UD",

    # Oviedo
    "Oviedo": "Real Oviedo",
    "Real Oviedo": "Real Oviedo",

    # Girona
    "Girona": "Girona FC",
    "Girona FC": "Girona FC",
}


# Función que normaliza un nombre de equipo
def normalize_team_name(team_name: str) -> str:
    # Elimina espacios al principio y al final
    team_name = team_name.strip()

    # Si el nombre está en el diccionario de alias, devuelve el oficial.
    # Si no, devuelve el mismo nombre recibido.
    return TEAM_ALIASES.get(team_name, team_name)


# Función que carga todo el archivo JSON de estadísticas
def load_team_stats() -> dict:
    # Abre el archivo en modo lectura con codificación UTF-8
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        # Convierte el JSON a un diccionario de Python
        return json.load(file)


# Función que devuelve todos los equipos disponibles
def get_all_teams() -> list:
    """
    Devuelve todos los equipos disponibles en el archivo JSON de estadísticas.

    Esta función se mantiene por compatibilidad, aunque el endpoint /api/teams
    ahora obtiene los equipos desde MySQL.
    """
    team_stats = load_team_stats()
    return sorted(team_stats.keys())


# Función que devuelve las estadísticas de un equipo concreto
def get_team_stats(team_name: str) -> dict:
    """
    Devuelve las estadísticas de un equipo concreto.

    Si el equipo no existe en el JSON, devuelve estadísticas por defecto
    para evitar que la predicción falle.
    """
    default_stats = {
        "puntos_recientes": 9,
        "goles_favor": 5,
        "goles_contra": 5,
        "rendimiento_casa": 5,
        "rendimiento_fuera": 5
    }

    team_stats = load_team_stats()
    normalized_name = normalize_team_name(team_name)

    return team_stats.get(normalized_name, default_stats)


# Función que prepara los datos de un partido completo
def get_match_data(local: str, visitante: str) -> dict:
    local_normalizado = normalize_team_name(local)
    visitante_normalizado = normalize_team_name(visitante)

    stats_local = get_team_stats(local_normalizado)
    stats_visitante = get_team_stats(visitante_normalizado)

    local_goles_favor = stats_local["goles_favor"]
    local_goles_contra = stats_local["goles_contra"]
    visitante_goles_favor = stats_visitante["goles_favor"]
    visitante_goles_contra = stats_visitante["goles_contra"]

    return {
        "local": local_normalizado,
        "visitante": visitante_normalizado,
        "stats_local": stats_local,
        "stats_visitante": stats_visitante,

        # Medias acumuladas base
        "local_goles_favor_avg": local_goles_favor,
        "local_goles_contra_avg": local_goles_contra,
        "local_tiros_avg": local_goles_favor * 3,
        "local_tiros_puerta_avg": local_goles_favor * 1.5,
        "local_corners_avg": stats_local["rendimiento_casa"],
        "local_faltas_avg": 10,
        "local_amarillas_avg": 2,
        "local_rojas_avg": 0.1,

        "visitante_goles_favor_avg": visitante_goles_favor,
        "visitante_goles_contra_avg": visitante_goles_contra,
        "visitante_tiros_avg": visitante_goles_favor * 3,
        "visitante_tiros_puerta_avg": visitante_goles_favor * 1.5,
        "visitante_corners_avg": stats_visitante["rendimiento_fuera"],
        "visitante_faltas_avg": 10,
        "visitante_amarillas_avg": 2,
        "visitante_rojas_avg": 0.1,

        # Últimos 5 partidos (aproximación temporal)
        "local_goles_favor_last5_avg": local_goles_favor,
        "local_goles_contra_last5_avg": local_goles_contra,
        "local_tiros_last5_avg": local_goles_favor * 3,
        "local_tiros_puerta_last5_avg": local_goles_favor * 1.5,
        "local_corners_last5_avg": stats_local["rendimiento_casa"],
        "local_faltas_last5_avg": 10,
        "local_amarillas_last5_avg": 2,
        "local_rojas_last5_avg": 0.1,
        "local_puntos_last5_avg": stats_local["puntos_recientes"] / 5,
        "local_racha_last5_avg": 0.4,

        "visitante_goles_favor_last5_avg": visitante_goles_favor,
        "visitante_goles_contra_last5_avg": visitante_goles_contra,
        "visitante_tiros_last5_avg": visitante_goles_favor * 3,
        "visitante_tiros_puerta_last5_avg": visitante_goles_favor * 1.5,
        "visitante_corners_last5_avg": stats_visitante["rendimiento_fuera"],
        "visitante_faltas_last5_avg": 10,
        "visitante_amarillas_last5_avg": 2,
        "visitante_rojas_last5_avg": 0.1,
        "visitante_puntos_last5_avg": stats_visitante["puntos_recientes"] / 5,
        "visitante_racha_last5_avg": 0.2
    }