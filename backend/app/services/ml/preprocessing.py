import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


CATEGORICAL_FEATURES = ["local", "visitante"]

NUMERIC_FEATURES = [
    "local_goles_favor_avg",
    "local_goles_contra_avg",
    "local_tiros_avg",
    "local_tiros_puerta_avg",
    "local_corners_avg",
    "local_faltas_avg",
    "local_amarillas_avg",
    "local_rojas_avg",
    "visitante_goles_favor_avg",
    "visitante_goles_contra_avg",
    "visitante_tiros_avg",
    "visitante_tiros_puerta_avg",
    "visitante_corners_avg",
    "visitante_faltas_avg",
    "visitante_amarillas_avg",
    "visitante_rojas_avg",

    "local_goles_favor_last5_avg",
    "local_goles_contra_last5_avg",
    "local_tiros_last5_avg",
    "local_tiros_puerta_last5_avg",
    "local_corners_last5_avg",
    "local_faltas_last5_avg",
    "local_amarillas_last5_avg",
    "local_rojas_last5_avg",
    "local_puntos_last5_avg",
    "local_racha_last5_avg",

    "visitante_goles_favor_last5_avg",
    "visitante_goles_contra_last5_avg",
    "visitante_tiros_last5_avg",
    "visitante_tiros_puerta_last5_avg",
    "visitante_corners_last5_avg",
    "visitante_faltas_last5_avg",
    "visitante_amarillas_last5_avg",
    "visitante_rojas_last5_avg",
    "visitante_puntos_last5_avg",
    "visitante_racha_last5_avg"
]

FEATURE_COLUMNS = CATEGORICAL_FEATURES + NUMERIC_FEATURES
TARGET_COLUMN = "resultado"


def build_preprocessor() -> ColumnTransformer:
    categorical_pipeline = Pipeline(
        steps=[
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ]
    )

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="mean")),
            ("scaler", StandardScaler())
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
            ("num", numeric_pipeline, NUMERIC_FEATURES)
        ],
        remainder="drop"
    )


def split_features_target(df: pd.DataFrame):
    missing_columns = [col for col in FEATURE_COLUMNS + [TARGET_COLUMN] if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Faltan columnas en el dataset: {missing_columns}")

    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()
    return X, y


def build_inference_frame(match_data: dict) -> pd.DataFrame:
    return pd.DataFrame([match_data])[FEATURE_COLUMNS]