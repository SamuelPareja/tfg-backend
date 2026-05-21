from pathlib import Path
import json

from app.services.ml.training import load_training_dataset
from app.services.ml.poisson_model import QuinielaPoissonModel, ARTIFACTS_DIR


DATASET_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "historical_matches.csv"
POISSON_METRICS_FILE = ARTIFACTS_DIR / "poisson_info.json"


def calibrate_and_save_poisson_model(dataset_path=DATASET_FILE):
    """
    Calcula parámetros base del modelo Poisson a partir del dataset histórico.
    """
    df = load_training_dataset(dataset_path)

    league_home_goals_avg = df["local_goles_favor_avg"].mean()
    league_away_goals_avg = df["visitante_goles_favor_avg"].mean()

    home_advantage_factor = 1.10

    config = {
        "league_home_goals_avg": round(float(league_home_goals_avg), 4),
        "league_away_goals_avg": round(float(league_away_goals_avg), 4),
        "home_advantage_factor": home_advantage_factor
    }

    model = QuinielaPoissonModel(config)
    model.save_config()

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    info = {
        "modelo": "poisson",
        "league_home_goals_avg": config["league_home_goals_avg"],
        "league_away_goals_avg": config["league_away_goals_avg"],
        "home_advantage_factor": config["home_advantage_factor"]
    }

    with open(POISSON_METRICS_FILE, "w", encoding="utf-8") as file:
        json.dump(info, file, indent=2, ensure_ascii=False)

    return info


if __name__ == "__main__":
    result = calibrate_and_save_poisson_model()
    print("Calibración Poisson completada correctamente.")
    print(result)