from app.services.ml.model import QuinielaMLModel
from app.services.ml.rf_model import QuinielaRFModel
from app.services.ml.poisson_model import QuinielaPoissonModel
from app.services.ml.preprocessing import build_inference_frame

from pathlib import Path
import json

ENSEMBLE_WEIGHTS_FILE = Path(__file__).resolve().parent / "ml" / "artifacts" / "ensemble_weights.json"

# “He implementado una métrica propia que calcula la fuerza de cada equipo en función de sus estadísticas.”

# “La fuerza del equipo se calcula combinando puntos recientes, goles a favor, goles en contra y 
# rendimiento en casa o fuera, aplicando distintos pesos.”

# “Después comparo la fuerza de ambos equipos y, según la diferencia,
#  determino si gana el local, hay empate o gana el visitante.”

# “La decisión no depende del modelo de inteligencia artificial, sino
#  de una métrica basada en datos.”

# Función que calcula la fuerza de un equipo a partir de sus estadísticas
def calculate_team_strength(stats: dict, is_home: bool) -> int:
    # Obtiene los valores del equipo
    puntos_recientes = stats["puntos_recientes"]
    goles_favor = stats["goles_favor"]
    goles_contra = stats["goles_contra"]

    # Usa el rendimiento en casa o fuera según corresponda
    rendimiento = stats["rendimiento_casa"] if is_home else stats["rendimiento_fuera"]

    # Fórmula de cálculo de fuerza
    # Se combinan diferentes factores con pesos
    fuerza = (
        puntos_recientes * 3
        + goles_favor * 2
        - goles_contra
        + rendimiento * 2
    )

    # Devuelve un número que representa la fuerza del equipo
    return fuerza


# Función principal que decide la predicción del partido
def calculate_prediction(match_data: dict) -> dict:
    # Obtiene las estadísticas del equipo local y visitante
    stats_local = match_data["stats_local"]
    stats_visitante = match_data["stats_visitante"]

    # Calcula la fuerza de ambos equipos
    fuerza_local = calculate_team_strength(stats_local, is_home=True)
    fuerza_visitante = calculate_team_strength(stats_visitante, is_home=False)

    # Calcula la diferencia de fuerzas
    diferencia = fuerza_local - fuerza_visitante

    # Lógica de decisión:
    # Si son muy parecidos → empate
    if abs(diferencia) <= 8:
        recomendacion = "X"
        motivo = "Los dos equipos llegan con números bastante parecidos."

    # Si el local es claramente mejor → gana local
    elif diferencia > 8:
        recomendacion = "1"
        motivo = "El equipo local presenta mejores estadísticas recientes."

    # Si el visitante es mejor → gana visitante
    else:
        recomendacion = "2"
        motivo = "El equipo visitante presenta mejores estadísticas recientes."

    # Devuelve toda la información calculada
    return {
        "recomendacion": recomendacion,
        "motivo": motivo,
        "fuerza_local": fuerza_local,
        "fuerza_visitante": fuerza_visitante,
        "diferencia": diferencia
    }


def predict_with_ml(match_data: dict) -> dict:
    """
    Realiza una predicción usando el modelo de machine learning.
    """
    model = QuinielaMLModel.load()

    X = build_inference_frame(match_data)

    probabilidades = model.predict_proba_dict(X)
    recomendacion = max(probabilidades, key=probabilidades.get)

    return {
        "recomendacion": recomendacion,
        "motivo": "Predicción generada por el modelo de machine learning con estadísticas históricas.",
        "probabilidades": probabilidades
    }


def predict_with_rf(match_data: dict) -> dict:
    """
    Realiza una predicción usando el modelo Random Forest.
    """
    model = QuinielaRFModel.load()

    X = build_inference_frame(match_data)

    probabilidades = model.predict_proba_dict(X)
    recomendacion = max(probabilidades, key=probabilidades.get)

    return {
        "recomendacion": recomendacion,
        "motivo": "Predicción generada por el modelo Random Forest con estadísticas históricas.",
        "probabilidades": probabilidades
    }


def predict_with_poisson(match_data: dict) -> dict:
    """
    Realiza una predicción usando el modelo Poisson.
    """
    model = QuinielaPoissonModel.load()

    prediction = model.predict_match(match_data)

    return prediction


# Función auxiliar para combinar probabilidades
def combine_probabilities(prob_ml: dict, prob_rf: dict, prob_poisson: dict, weights: dict) -> dict:
    prob_1 = (
        weights["ml"] * prob_ml["1"] +
        weights["rf"] * prob_rf["1"] +
        weights["poisson"] * prob_poisson["1"]
    )

    prob_x = (
        weights["ml"] * prob_ml["X"] +
        weights["rf"] * prob_rf["X"] +
        weights["poisson"] * prob_poisson["X"]
    )

    prob_2 = (
        weights["ml"] * prob_ml["2"] +
        weights["rf"] * prob_rf["2"] +
        weights["poisson"] * prob_poisson["2"]
    )

    total = prob_1 + prob_x + prob_2

    if total > 0:
        prob_1 /= total
        prob_x /= total
        prob_2 /= total

    return {
        "1": round(prob_1, 4),
        "X": round(prob_x, 4),
        "2": round(prob_2, 4)
    }


def load_optimized_ensemble_weights() -> dict:
    """
    Carga pesos optimizados si existen.
    Si no existen, devuelve los pesos manuales por defecto.
    """
    default_weights = {
        "ml": 0.25,
        "rf": 0.35,
        "poisson": 0.40
    }

    if not ENSEMBLE_WEIGHTS_FILE.exists():
        return default_weights

    with open(ENSEMBLE_WEIGHTS_FILE, "r", encoding="utf-8") as file:
        payload = json.load(file)

    return payload.get("recommended_weights", default_weights)


# Modo Ensemble
def predict_with_ensemble(match_data: dict) -> dict:
    weights = load_optimized_ensemble_weights()

    ml_prediction = predict_with_ml(match_data)
    rf_prediction = predict_with_rf(match_data)
    poisson_prediction = predict_with_poisson(match_data)

    final_probabilities = combine_probabilities(
        prob_ml=ml_prediction["probabilidades"],
        prob_rf=rf_prediction["probabilidades"],
        prob_poisson=poisson_prediction["probabilidades"],
        weights=weights
    )

    recomendacion = max(final_probabilities, key=final_probabilities.get)

    return {
        "recomendacion": recomendacion,
        "motivo": "Predicción generada mediante ensemble manual combinando ML, Random Forest y Poisson.",
        "probabilidades": final_probabilities,
        "model_outputs": {
            "ml": ml_prediction,
            "rf": rf_prediction,
            "poisson": poisson_prediction
        },
        "ensemble_weights": weights
    }    