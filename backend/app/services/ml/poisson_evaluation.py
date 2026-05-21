from pathlib import Path
import json
import math

from sklearn.metrics import accuracy_score, log_loss

from app.services.ml.training import load_training_dataset
from app.services.ml.poisson_model import QuinielaPoissonModel, ARTIFACTS_DIR


DATASET_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "historical_matches.csv"
POISSON_METRICS_FILE = ARTIFACTS_DIR / "poisson_metrics.json"


LABELS = ["1", "X", "2"]


def evaluate_poisson_model(dataset_path=DATASET_FILE):
    """
    Evalúa el modelo Poisson en todo el dataset histórico.
    """
    df = load_training_dataset(dataset_path)
    model = QuinielaPoissonModel.load()

    y_true = []
    y_pred = []
    y_prob = []

    for _, row in df.iterrows():
        match_data = row.to_dict()

        probabilities = model.predict_proba_dict(match_data)

        pred_label = max(probabilities, key=probabilities.get)
        true_label = row["resultado"]

        y_true.append(true_label)
        y_pred.append(pred_label)
        y_prob.append([
            probabilities.get("1", 0.0),
            probabilities.get("X", 0.0),
            probabilities.get("2", 0.0)
        ])

    accuracy = accuracy_score(y_true, y_pred)
    loss = log_loss(y_true, y_prob, labels=LABELS)

    metrics = {
        "model": "poisson",
        "samples": len(y_true),
        "accuracy": round(float(accuracy), 4),
        "log_loss": round(float(loss), 4)
    }

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    with open(POISSON_METRICS_FILE, "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2, ensure_ascii=False)

    return metrics


if __name__ == "__main__":
    result = evaluate_poisson_model()
    print("Evaluación Poisson completada correctamente.")
    print(result)