import pandas as pd
from pathlib import Path


# Archivo fuente completo
SOURCE_FILE = Path("app/data/SP1.csv")

# Archivo procesado para el modelo ML
OUTPUT_FILE = Path("app/data/historical_matches.csv")


def normalize_result(value: str) -> str:
    """
    Convierte:
    H -> 1
    D -> X
    A -> 2
    """
    mapping = {
        "H": "1",
        "D": "X",
        "A": "2"
    }
    return mapping.get(value)


def compute_points_and_form(is_home: bool, ftr_value: str):
    """
    Calcula:
    - puntos del equipo en ese partido
    - valor de racha:
      victoria = 1
      empate = 0
      derrota = -1
    """
    if is_home:
        if ftr_value == "H":
            return 3, 1
        if ftr_value == "D":
            return 1, 0
        return 0, -1

    if ftr_value == "A":
        return 3, 1
    if ftr_value == "D":
        return 1, 0
    return 0, -1


def create_team_match_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte cada partido en dos filas:
    una para el local y otra para el visitante.
    """
    home_points_and_form = df["FTR"].apply(lambda x: compute_points_and_form(True, x))
    away_points_and_form = df["FTR"].apply(lambda x: compute_points_and_form(False, x))

    home_df = pd.DataFrame({
        "Date": df["Date"],
        "team": df["HomeTeam"],
        "goles_favor": df["FTHG"],
        "goles_contra": df["FTAG"],
        "tiros": df["HS"],
        "tiros_puerta": df["HST"],
        "corners": df["HC"],
        "faltas": df["HF"],
        "amarillas": df["HY"],
        "rojas": df["HR"],
        "puntos": [value[0] for value in home_points_and_form],
        "racha": [value[1] for value in home_points_and_form]
    })

    away_df = pd.DataFrame({
        "Date": df["Date"],
        "team": df["AwayTeam"],
        "goles_favor": df["FTAG"],
        "goles_contra": df["FTHG"],
        "tiros": df["AS"],
        "tiros_puerta": df["AST"],
        "corners": df["AC"],
        "faltas": df["AF"],
        "amarillas": df["AY"],
        "rojas": df["AR"],
        "puntos": [value[0] for value in away_points_and_form],
        "racha": [value[1] for value in away_points_and_form]
    })

    team_matches = pd.concat([home_df, away_df], ignore_index=True)
    team_matches = team_matches.sort_values(["team", "Date"]).reset_index(drop=True)

    return team_matches


def compute_expanding_averages(team_matches: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula medias históricas acumuladas usando solo partidos anteriores.
    """
    stat_columns = [
        "goles_favor",
        "goles_contra",
        "tiros",
        "tiros_puerta",
        "corners",
        "faltas",
        "amarillas",
        "rojas"
    ]

    result = team_matches.copy()

    for column in stat_columns:
        result[f"{column}_avg"] = (
            result.groupby("team")[column]
            .transform(lambda s: s.shift(1).expanding().mean())
        )

    return result


def compute_last5_averages(team_matches: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula medias de los últimos 5 partidos anteriores.
    """
    stat_columns = [
        "goles_favor",
        "goles_contra",
        "tiros",
        "tiros_puerta",
        "corners",
        "faltas",
        "amarillas",
        "rojas",
        "puntos",
        "racha"
    ]

    result = team_matches.copy()

    for column in stat_columns:
        result[f"{column}_last5_avg"] = (
            result.groupby("team")[column]
            .transform(lambda s: s.shift(1).rolling(window=5, min_periods=1).mean())
        )

    return result


def main():
    # 1. Cargar CSV original
    df = pd.read_csv(SOURCE_FILE)

    # 2. Quedarnos solo con columnas fuente necesarias
    df = df[
        [
            "Date",
            "HomeTeam",
            "AwayTeam",
            "FTR",
            "FTHG",
            "FTAG",
            "HS",
            "AS",
            "HST",
            "AST",
            "HC",
            "AC",
            "HF",
            "AF",
            "HY",
            "AY",
            "HR",
            "AR"
        ]
    ].copy()

    # 3. Convertir fecha
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

    # 4. Convertir resultado al formato del proyecto
    df["resultado"] = df["FTR"].map(normalize_result)

    # 5. Eliminar filas con datos clave incompletos
    df = df.dropna(subset=["Date", "HomeTeam", "AwayTeam", "resultado"])

    # 6. Crear dataset por equipo
    team_matches = create_team_match_rows(df)

    # 7. Calcular medias históricas acumuladas
    team_matches = compute_expanding_averages(team_matches)

    # 8. Calcular medias de últimos 5 partidos
    team_matches = compute_last5_averages(team_matches)

    # 9. Preparar merge para local
    local_stats = team_matches.rename(columns={
        "team": "local",
        "goles_favor_avg": "local_goles_favor_avg",
        "goles_contra_avg": "local_goles_contra_avg",
        "tiros_avg": "local_tiros_avg",
        "tiros_puerta_avg": "local_tiros_puerta_avg",
        "corners_avg": "local_corners_avg",
        "faltas_avg": "local_faltas_avg",
        "amarillas_avg": "local_amarillas_avg",
        "rojas_avg": "local_rojas_avg",
        "goles_favor_last5_avg": "local_goles_favor_last5_avg",
        "goles_contra_last5_avg": "local_goles_contra_last5_avg",
        "tiros_last5_avg": "local_tiros_last5_avg",
        "tiros_puerta_last5_avg": "local_tiros_puerta_last5_avg",
        "corners_last5_avg": "local_corners_last5_avg",
        "faltas_last5_avg": "local_faltas_last5_avg",
        "amarillas_last5_avg": "local_amarillas_last5_avg",
        "rojas_last5_avg": "local_rojas_last5_avg",
        "puntos_last5_avg": "local_puntos_last5_avg",
        "racha_last5_avg": "local_racha_last5_avg"
    })[
        [
            "Date",
            "local",
            "local_goles_favor_avg",
            "local_goles_contra_avg",
            "local_tiros_avg",
            "local_tiros_puerta_avg",
            "local_corners_avg",
            "local_faltas_avg",
            "local_amarillas_avg",
            "local_rojas_avg",
            "local_goles_favor_last5_avg",
            "local_goles_contra_last5_avg",
            "local_tiros_last5_avg",
            "local_tiros_puerta_last5_avg",
            "local_corners_last5_avg",
            "local_faltas_last5_avg",
            "local_amarillas_last5_avg",
            "local_rojas_last5_avg",
            "local_puntos_last5_avg",
            "local_racha_last5_avg"
        ]
    ]

    # 10. Preparar merge para visitante
    visitante_stats = team_matches.rename(columns={
        "team": "visitante",
        "goles_favor_avg": "visitante_goles_favor_avg",
        "goles_contra_avg": "visitante_goles_contra_avg",
        "tiros_avg": "visitante_tiros_avg",
        "tiros_puerta_avg": "visitante_tiros_puerta_avg",
        "corners_avg": "visitante_corners_avg",
        "faltas_avg": "visitante_faltas_avg",
        "amarillas_avg": "visitante_amarillas_avg",
        "rojas_avg": "visitante_rojas_avg",
        "goles_favor_last5_avg": "visitante_goles_favor_last5_avg",
        "goles_contra_last5_avg": "visitante_goles_contra_last5_avg",
        "tiros_last5_avg": "visitante_tiros_last5_avg",
        "tiros_puerta_last5_avg": "visitante_tiros_puerta_last5_avg",
        "corners_last5_avg": "visitante_corners_last5_avg",
        "faltas_last5_avg": "visitante_faltas_last5_avg",
        "amarillas_last5_avg": "visitante_amarillas_last5_avg",
        "rojas_last5_avg": "visitante_rojas_last5_avg",
        "puntos_last5_avg": "visitante_puntos_last5_avg",
        "racha_last5_avg": "visitante_racha_last5_avg"
    })[
        [
            "Date",
            "visitante",
            "visitante_goles_favor_avg",
            "visitante_goles_contra_avg",
            "visitante_tiros_avg",
            "visitante_tiros_puerta_avg",
            "visitante_corners_avg",
            "visitante_faltas_avg",
            "visitante_amarillas_avg",
            "visitante_rojas_avg",
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
    ]

    # 11. Base del dataset final
    matches_df = pd.DataFrame({
        "Date": df["Date"],
        "local": df["HomeTeam"],
        "visitante": df["AwayTeam"],
        "resultado": df["resultado"]
    })

    # 12. Merge local
    matches_df = matches_df.merge(
        local_stats,
        on=["Date", "local"],
        how="left"
    )

    # 13. Merge visitante
    matches_df = matches_df.merge(
        visitante_stats,
        on=["Date", "visitante"],
        how="left"
    )

    # 14. Eliminar filas vacías
    matches_df = matches_df.dropna()

    # 15. Guardar dataset final
    matches_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print("CSV PRO+ generado correctamente.")
    print(f"Archivo original conservado en: {SOURCE_FILE}")
    print(f"Archivo procesado generado en: {OUTPUT_FILE}")
    print(f"Filas finales para entrenamiento: {len(matches_df)}")


if __name__ == "__main__":
    main()