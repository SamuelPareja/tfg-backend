from pathlib import Path
import json
from sklearn.model_selection import train_test_split

from app.services.ml.preprocessing import split_features_target
from app.services.ml.training import load_training_dataset
from app.services.ml.evaluation import evaluate_model
from app.services.ml.rf_model import QuinielaRFModel, ARTIFACTS_DIR


# Ruta al dataset histórico ya transformado
DATASET_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "historical_matches.csv"

# Archivo donde guardaremos las métricas del RF
RF_METRICS_FILE = ARTIFACTS_DIR / "rf_metrics.json"


def train_and_save_rf_model(test_size=0.3, random_state=42, dataset_path=DATASET_FILE):
    """
    Entrena y guarda el modelo Random Forest.

    Usa:
    - el mismo dataset que el modelo ML actual
    - la misma separación train/validation
    - la misma evaluación (accuracy y log_loss)
    """
    df = load_training_dataset(dataset_path)

    X, y = split_features_target(df)

    X_train, X_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    model = QuinielaRFModel()
    model.fit(X_train, y_train)

    metrics = evaluate_model(model, X_val, y_val)

    model.save()

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "train_size": len(X_train),
        "validation_size": len(X_val),
        **metrics
    }

    with open(RF_METRICS_FILE, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)

    return payload


if __name__ == "__main__":
    result = train_and_save_rf_model()
    print("Entrenamiento RF completado correctamente.")
    print(result)