from pathlib import Path
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

from app.services.ml.preprocessing import build_preprocessor


# Carpeta donde se guardarán los artefactos entrenados
ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"
PREPROCESSOR_FILE = ARTIFACTS_DIR / "preprocessor.joblib"
MODEL_FILE = ARTIFACTS_DIR / "model.joblib"
LABEL_ENCODER_FILE = ARTIFACTS_DIR / "label_encoder.joblib"


class QuinielaMLModel:
    """
    Modelo multiclase para quinielas.

    Usa:
    - OneHotEncoder para codificar equipos
    - LogisticRegression multinomial para clasificación multiclase

    En el caso multinomial, LogisticRegression produce probabilidades
    mediante una capa softmax sobre las tres clases.
    """

    def __init__(self, preprocessor=None, classifier=None, label_encoder=None):
        self.preprocessor = preprocessor or build_preprocessor()
        self.classifier = classifier or LogisticRegression(   
            solver="lbfgs",
            max_iter=3000,
            random_state=42
        )
        self.label_encoder = label_encoder or LabelEncoder()

    def fit(self, X_train, y_train):
        """
        Entrena el preprocesador y el modelo.
        """
        y_encoded = self.label_encoder.fit_transform(y_train)
        X_train_transformed = self.preprocessor.fit_transform(X_train)
        self.classifier.fit(X_train_transformed, y_encoded)
        return self

    def predict(self, X):
        """
        Devuelve la clase predicha: 1, X o 2.
        """
        X_transformed = self.preprocessor.transform(X)
        y_pred_encoded = self.classifier.predict(X_transformed)
        return self.label_encoder.inverse_transform(y_pred_encoded)

    def predict_proba_matrix(self, X):
        """
        Devuelve la matriz de probabilidades en el orden interno del clasificador.
        """
        X_transformed = self.preprocessor.transform(X)
        return self.classifier.predict_proba(X_transformed)

    def get_classifier_labels(self):
        """
        Devuelve las etiquetas reales en el mismo orden que el clasificador.
        """
        return list(self.label_encoder.inverse_transform(self.classifier.classes_))

    def predict_proba(self, X):
        """
        Devuelve una lista con probabilidades en este orden fijo:
        [p1, pX, p2]
        """
        probability_map = self.predict_proba_dict(X)
        return [
            probability_map.get("1", 0.0),
            probability_map.get("X", 0.0),
            probability_map.get("2", 0.0)
        ]

    def predict_proba_dict(self, X):
        """
        Devuelve las probabilidades en formato diccionario:
        {
          "1": 0.55,
          "X": 0.25,
          "2": 0.20
        }
        """
        probabilities = self.predict_proba_matrix(X)[0]
        labels = self.get_classifier_labels()

        probability_map = {
            label: float(prob)
            for label, prob in zip(labels, probabilities)
        }

        return {
            "1": round(probability_map.get("1", 0.0), 4),
            "X": round(probability_map.get("X", 0.0), 4),
            "2": round(probability_map.get("2", 0.0), 4)
        }

    def save(self):
        """
        Guarda preprocesador, clasificador y codificador de etiquetas.
        """
        ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

        joblib.dump(self.preprocessor, PREPROCESSOR_FILE)
        joblib.dump(self.classifier, MODEL_FILE)
        joblib.dump(self.label_encoder, LABEL_ENCODER_FILE)

    @classmethod
    def load(cls):
        """
        Carga los artefactos entrenados desde disco.
        """
        if not PREPROCESSOR_FILE.exists() or not MODEL_FILE.exists() or not LABEL_ENCODER_FILE.exists():
            raise FileNotFoundError(
                "No se ha encontrado el modelo entrenado. Ejecuta primero el entrenamiento."
            )

        preprocessor = joblib.load(PREPROCESSOR_FILE)
        classifier = joblib.load(MODEL_FILE)
        label_encoder = joblib.load(LABEL_ENCODER_FILE)

        return cls(
            preprocessor=preprocessor,
            classifier=classifier,
            label_encoder=label_encoder
        )