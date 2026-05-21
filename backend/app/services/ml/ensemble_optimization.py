from pathlib import Path
import json

from sklearn.metrics import accuracy_score, log_loss

from app.services.ml.training import load_training_dataset
from app.services.ml.model import QuinielaMLModel
from app.services.ml.rf_model import QuinielaRFModel
from app.services.ml.poisson_model import QuinielaPoissonModel
from app.services.prediction_service import combine_probabilities
from app.services.ml.preprocessing import split_features_target


ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"
DATASET_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "historical_matches.csv"
ENSEMBLE_WEIGHTS_FILE = ARTIFACTS_DIR / "ensemble_weights.json"

LABELS = ["1", "2", "X"]


def normalize_probabilities(probabilities: dict) -> dict:
    total = probabilities["1"] + probabilities["X"] + probabilities["2"]

    if total <= 0:
        return {"1": 1/3, "X": 1/3, "2": 1/3}

    return {
        "1": probabilities["1"] / total,
        "X": probabilities["X"] / total,
        "2": probabilities["2"] / total
    }


def generate_weight_combinations(step=0.1):
    combinations = []

    values = [round(i * step, 10) for i in range(int(1 / step) + 1)]

    for ml_weight in values:
        for rf_weight in values:
            poisson_weight = round(1.0 - ml_weight - rf_weight, 10)

            if poisson_weight < 0 or poisson_weight > 1:
                continue

            total = round(ml_weight + rf_weight + poisson_weight, 10)

            if total == 1.0:
                combinations.append({
                    "ml": round(ml_weight, 2),
                    "rf": round(rf_weight, 2),
                    "poisson": round(poisson_weight, 2)
                })

    return combinations


def precompute_model_probabilities(df, ml_model, rf_model, poisson_model):
    """
    Calcula una sola vez las probabilidades de cada modelo
    para todas las filas del dataset.
    """
    X, y = split_features_target(df)

    cached_rows = []

    total_rows = len(X)

    for index, (idx, row) in enumerate(X.iterrows(), start=1):
        row_df = X.loc[[idx]]
        row_dict = row.to_dict()

        ml_prob = ml_model.predict_proba_dict(row_df)
        rf_prob = rf_model.predict_proba_dict(row_df)
        poisson_prob = poisson_model.predict_proba_dict(row_dict)

        cached_rows.append({
            "y_true": y.loc[idx],
            "ml": ml_prob,
            "rf": rf_prob,
            "poisson": poisson_prob
        })

        if index % 200 == 0 or index == total_rows:
            print(f"Probabilidades precalculadas: {index}/{total_rows}")

    return cached_rows


def evaluate_weights(weights: dict, cached_rows: list):
    """
    Evalúa una combinación de pesos usando probabilidades ya precalculadas.
    """
    y_true = []
    y_pred = []
    y_prob = []

    for row in cached_rows:
        combined = combine_probabilities(
            prob_ml=row["ml"],
            prob_rf=row["rf"],
            prob_poisson=row["poisson"],
            weights=weights
        )

        combined = normalize_probabilities(combined)

        pred_label = max(combined, key=combined.get)

        y_true.append(row["y_true"])
        y_pred.append(pred_label)
        y_prob.append([
            combined["1"],
            combined["2"],
            combined["X"]
        ])

    accuracy = accuracy_score(y_true, y_pred)
    loss = log_loss(y_true, y_prob, labels=LABELS)

    return {
        "accuracy": round(float(accuracy), 4),
        "log_loss": round(float(loss), 4)
    }


def optimize_ensemble_weights(step=0.1):
    df = load_training_dataset(DATASET_FILE)

    ml_model = QuinielaMLModel.load()
    rf_model = QuinielaRFModel.load()
    poisson_model = QuinielaPoissonModel.load()

    print("Precalculando probabilidades de ML, RF y Poisson...")
    cached_rows = precompute_model_probabilities(df, ml_model, rf_model, poisson_model)

    weight_combinations = generate_weight_combinations(step=step)

    best_by_accuracy = None
    best_by_log_loss = None

    total_combinations = len(weight_combinations)

    for index, weights in enumerate(weight_combinations, start=1):
        metrics = evaluate_weights(weights, cached_rows)

        result = {
            "weights": weights,
            "accuracy": metrics["accuracy"],
            "log_loss": metrics["log_loss"]
        }

        if best_by_accuracy is None:
            best_by_accuracy = result
        elif metrics["accuracy"] > best_by_accuracy["accuracy"]:
            best_by_accuracy = result

        if best_by_log_loss is None:
            best_by_log_loss = result
        elif metrics["log_loss"] < best_by_log_loss["log_loss"]:
            best_by_log_loss = result

        if index % 10 == 0 or index == total_combinations:
            print(f"Combinaciones evaluadas: {index}/{total_combinations}")

    payload = {
        "step": step,
        "total_combinations": len(weight_combinations),
        "best_by_accuracy": best_by_accuracy,
        "best_by_log_loss": best_by_log_loss,
        "recommended_weights": best_by_log_loss["weights"]
    }

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    with open(ENSEMBLE_WEIGHTS_FILE, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)

    print("\n=== OPTIMIZACIÓN DE PESOS DEL ENSEMBLE ===")
    print(f"Combinaciones probadas: {payload['total_combinations']}")
    print(f"Mejor accuracy -> pesos: {best_by_accuracy['weights']}, accuracy: {best_by_accuracy['accuracy']}, log_loss: {best_by_accuracy['log_loss']}")
    print(f"Mejor log_loss -> pesos: {best_by_log_loss['weights']}, accuracy: {best_by_log_loss['accuracy']}, log_loss: {best_by_log_loss['log_loss']}")
    print(f"Pesos recomendados: {payload['recommended_weights']}")

    return payload


if __name__ == "__main__":
    optimize_ensemble_weights(step=0.1)