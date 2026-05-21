from pathlib import Path
import json
import pandas as pd
from sklearn.model_selection import train_test_split

from app.services.ml.preprocessing import split_features_target
from app.services.ml.model import QuinielaMLModel, ARTIFACTS_DIR
from app.services.ml.evaluation import evaluate_model


# Ruta al dataset de entrenamiento
DATASET_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "historical_matches.csv"

# Archivo donde guardaremos métricas del entrenamiento
METRICS_FILE = ARTIFACTS_DIR / "metrics.json"


def load_training_dataset(dataset_path=DATASET_FILE):
    """
    Carga el dataset histórico desde CSV.
    """
    dataset_path = Path(dataset_path)

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"No se ha encontrado el dataset de entrenamiento: {dataset_path}"
        )

    return pd.read_csv(dataset_path)


def train_and_save_model(test_size=0.3, random_state=42, dataset_path=DATASET_FILE):
    """
    Entrena y guarda el modelo ML.

    Importante:
    - separamos train y validation para medir generalización real
    - evitamos data leakage ajustando el preprocesador solo con train
    - el modelo multinomial usa internamente cross-entropy (log loss)
      como función de pérdida, que es la adecuada para clasificación
      multiclase con salida softmax
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

    model = QuinielaMLModel()
    model.fit(X_train, y_train)

    metrics = evaluate_model(model, X_val, y_val)

    model.save()

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "train_size": len(X_train),
        "validation_size": len(X_val),
        **metrics
    }

    with open(METRICS_FILE, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)

    return payload


if __name__ == "__main__":
    result = train_and_save_model()
    print("Entrenamiento completado correctamente.")
    print(result)