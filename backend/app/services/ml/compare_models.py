from pathlib import Path
import json

from app.services.ml.training import train_and_save_model
from app.services.ml.rf_training import train_and_save_rf_model
from app.services.ml.model import ARTIFACTS_DIR as ML_ARTIFACTS_DIR
from app.services.ml.rf_model import ARTIFACTS_DIR as RF_ARTIFACTS_DIR


ML_METRICS_FILE = ML_ARTIFACTS_DIR / "metrics.json"
RF_METRICS_FILE = RF_ARTIFACTS_DIR / "rf_metrics.json"


def load_json_file(path: Path):
    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def compare_metrics(ml_metrics: dict, rf_metrics: dict):
    comparison = {
        "ml": {
            "accuracy": ml_metrics.get("accuracy"),
            "log_loss": ml_metrics.get("log_loss"),
        },
        "rf": {
            "accuracy": rf_metrics.get("accuracy"),
            "log_loss": rf_metrics.get("log_loss"),
        },
        "winner_accuracy": "ml" if ml_metrics.get("accuracy", 0) > rf_metrics.get("accuracy", 0) else "rf",
        "winner_log_loss": "ml" if ml_metrics.get("log_loss", 999) < rf_metrics.get("log_loss", 999) else "rf"
    }

    return comparison


def run_comparison(retrain=False):
    if retrain:
        print("Reentrenando modelo ML...")
        train_and_save_model()

        print("Reentrenando modelo RF...")
        train_and_save_rf_model()

    ml_metrics = load_json_file(ML_METRICS_FILE)
    rf_metrics = load_json_file(RF_METRICS_FILE)

    if ml_metrics is None:
        raise FileNotFoundError("No existe metrics.json del modelo ML. Entrena primero el modelo ML.")

    if rf_metrics is None:
        raise FileNotFoundError("No existe rf_metrics.json del modelo RF. Entrena primero el modelo RF.")

    comparison = compare_metrics(ml_metrics, rf_metrics)

    print("\n=== COMPARACIÓN DE MODELOS ===")
    print(f"ML  -> accuracy: {comparison['ml']['accuracy']}, log_loss: {comparison['ml']['log_loss']}")
    print(f"RF  -> accuracy: {comparison['rf']['accuracy']}, log_loss: {comparison['rf']['log_loss']}")
    print(f"Mejor accuracy: {comparison['winner_accuracy']}")
    print(f"Mejor log_loss: {comparison['winner_log_loss']}")

    return comparison


if __name__ == "__main__":
    run_comparison(retrain=False)