from pathlib import Path
import json
import math


ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"
POISSON_CONFIG_FILE = ARTIFACTS_DIR / "poisson_config.json"


class QuinielaPoissonModel:
    def __init__(self, config: dict):
        self.config = config

    @staticmethod
    def poisson_pmf(k: int, lam: float) -> float:
        """
        Probabilidad de marcar exactamente k goles
        usando distribución de Poisson.
        """
        if lam <= 0:
            return 1.0 if k == 0 else 0.0

        return (math.exp(-lam) * (lam ** k)) / math.factorial(k)

    def estimate_expected_goals(self, match_data: dict):
        """
        Calcula goles esperados para local y visitante.
        """
        league_home_goals = self.config["league_home_goals_avg"]
        league_away_goals = self.config["league_away_goals_avg"]
        home_advantage = self.config.get("home_advantage_factor", 1.0)

        local_attack = (
            0.7 * match_data["local_goles_favor_avg"] +
            0.3 * match_data["local_goles_favor_last5_avg"]
        )

        local_defense = (
            0.7 * match_data["local_goles_contra_avg"] +
            0.3 * match_data["local_goles_contra_last5_avg"]
        )

        visitante_attack = (
            0.7 * match_data["visitante_goles_favor_avg"] +
            0.3 * match_data["visitante_goles_favor_last5_avg"]
        )

        visitante_defense = (
            0.7 * match_data["visitante_goles_contra_avg"] +
            0.3 * match_data["visitante_goles_contra_last5_avg"]
        )

        home_attack_strength = local_attack / max(league_home_goals, 0.01)
        away_attack_strength = visitante_attack / max(league_away_goals, 0.01)

        home_defense_weakness = visitante_defense / max(league_home_goals, 0.01)
        away_defense_weakness = local_defense / max(league_away_goals, 0.01)

        lambda_home = league_home_goals * home_attack_strength * home_defense_weakness * home_advantage
        lambda_away = league_away_goals * away_attack_strength * away_defense_weakness

        lambda_home = max(lambda_home, 0.05)
        lambda_away = max(lambda_away, 0.05)

        return round(lambda_home, 4), round(lambda_away, 4)

    def predict_proba_dict(self, match_data: dict, max_goals: int = 6):
        """
        Convierte los goles esperados en probabilidades 1 / X / 2.
        """
        lambda_home, lambda_away = self.estimate_expected_goals(match_data)

        p_home = [self.poisson_pmf(i, lambda_home) for i in range(max_goals + 1)]
        p_away = [self.poisson_pmf(j, lambda_away) for j in range(max_goals + 1)]

        prob_1 = 0.0
        prob_x = 0.0
        prob_2 = 0.0

        for i in range(max_goals + 1):
            for j in range(max_goals + 1):
                p = p_home[i] * p_away[j]

                if i > j:
                    prob_1 += p
                elif i == j:
                    prob_x += p
                else:
                    prob_2 += p

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

    def predict_match(self, match_data: dict):
        """
        Devuelve recomendación, probabilidades y goles esperados.
        """
        probabilities = self.predict_proba_dict(match_data)
        lambda_home, lambda_away = self.estimate_expected_goals(match_data)

        recomendacion = max(probabilities, key=probabilities.get)

        return {
            "recomendacion": recomendacion,
            "motivo": "Predicción generada por un modelo Poisson a partir de goles esperados.",
            "probabilidades": probabilities,
            "goles_esperados": {
                "local": lambda_home,
                "visitante": lambda_away
            }
        }

    def save_config(self):
        ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

        with open(POISSON_CONFIG_FILE, "w", encoding="utf-8") as file:
            json.dump(self.config, file, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls):
        if not POISSON_CONFIG_FILE.exists():
            raise FileNotFoundError(
                "No se ha encontrado la configuración Poisson. Ejecuta primero la calibración Poisson."
            )

        with open(POISSON_CONFIG_FILE, "r", encoding="utf-8") as file:
            config = json.load(file)

        return cls(config)
