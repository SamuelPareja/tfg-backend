from pathlib import Path
import json

from app.services.ml.training import train_and_save_model
from app.services.ml.rf_training import train_and_save_rf_model
from app.services.ml.poisson_training import calibrate_and_save_poisson_model
from app.services.ml.poisson_evaluation import evaluate_poisson_model
from app.services.ml.model import ARTIFACTS_DIR as ML_ARTIFACTS_DIR
from app.services.ml.rf_model import ARTIFACTS_DIR as RF_ARTIFACTS_DIR
from app.services.ml.poisson_model import ARTIFACTS_DIR as POISSON_ARTIFACTS_DIR


ML_METRICS_FILE = ML_ARTIFACTS_DIR / "metrics.json"
RF_METRICS_FILE = RF_ARTIFACTS_DIR / "rf_metrics.json"
POISSON_METRICS_FILE = POISSON_ARTIFACTS_DIR / "poisson_metrics.json"


def load_json_file(path: Path):
    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_best_accuracy(metrics_map: dict):
    return max(metrics_map, key=lambda name: metrics_map[name]["accuracy"])


def get_best_log_loss(metrics_map: dict):
    return min(metrics_map, key=lambda name: metrics_map[name]["log_loss"])


def compare_all_models(retrain=False):
    if retrain:
        print("Reentrenando ML...")
        train_and_save_model()

        print("Reentrenando RF...")
        train_and_save_rf_model()

        print("Recalibrando Poisson...")
        calibrate_and_save_poisson_model()

        print("Evaluando Poisson...")
        evaluate_poisson_model()

    ml_metrics = load_json_file(ML_METRICS_FILE)
    rf_metrics = load_json_file(RF_METRICS_FILE)
    poisson_metrics = load_json_file(POISSON_METRICS_FILE)

    if ml_metrics is None:
        raise FileNotFoundError("No existe metrics.json del modelo ML.")

    if rf_metrics is None:
        raise FileNotFoundError("No existe rf_metrics.json del modelo RF.")

    if poisson_metrics is None:
        raise FileNotFoundError("No existe poisson_metrics.json del modelo Poisson.")

    metrics_map = {
        "ml": {
            "accuracy": ml_metrics["accuracy"],
            "log_loss": ml_metrics["log_loss"]
        },
        "rf": {
            "accuracy": rf_metrics["accuracy"],
            "log_loss": rf_metrics["log_loss"]
        },
        "poisson": {
            "accuracy": poisson_metrics["accuracy"],
            "log_loss": poisson_metrics["log_loss"]
        }
    }

    comparison = {
        "ml": metrics_map["ml"],
        "rf": metrics_map["rf"],
        "poisson": metrics_map["poisson"],
        "winner_accuracy": get_best_accuracy(metrics_map),
        "winner_log_loss": get_best_log_loss(metrics_map)
    }

    print("\n=== COMPARACIÓN GLOBAL DE MODELOS ===")
    print(f"ML      -> accuracy: {comparison['ml']['accuracy']}, log_loss: {comparison['ml']['log_loss']}")
    print(f"RF      -> accuracy: {comparison['rf']['accuracy']}, log_loss: {comparison['rf']['log_loss']}")
    print(f"Poisson -> accuracy: {comparison['poisson']['accuracy']}, log_loss: {comparison['poisson']['log_loss']}")
    print(f"Mejor accuracy: {comparison['winner_accuracy']}")
    print(f"Mejor log_loss: {comparison['winner_log_loss']}")

    return comparison


if __name__ == "__main__":
    compare_all_models(retrain=False)