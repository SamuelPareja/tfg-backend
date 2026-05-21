from fastapi import APIRouter, HTTPException
from app.schemas import QuinielaRequest, QuinielaResponse, MatchPrediction
from app.services.data_service import get_match_data
from app.services.prediction_service import (
    calculate_prediction,
    predict_with_ml,
    predict_with_rf,
    predict_with_poisson,
    predict_with_ensemble
)
from app.services.ollama_service import ask_ollama

router = APIRouter()


@router.post("/predict", response_model=QuinielaResponse)
def predict_quiniela(data: QuinielaRequest, mode: str = "classic"):
    if mode not in ["classic", "ml", "rf", "poisson", "ensemble"]:
        raise HTTPException(
            status_code=400,
            detail="El parámetro mode debe ser 'classic', 'ml', 'rf', 'poisson' o 'ensemble'."
        )

    resultados = []

    for partido in data.partidos:
        match_data = get_match_data(partido.local, partido.visitante)

        if mode == "classic":
            prediction_data = calculate_prediction(match_data)
        elif mode == "ml":
            try:
                prediction_data = predict_with_ml(match_data)
            except FileNotFoundError as exc:
                raise HTTPException(
                    status_code=400,
                    detail=str(exc)
                ) from exc
        elif mode == "rf":
            try:
                prediction_data = predict_with_rf(match_data)
            except FileNotFoundError as exc:
                raise HTTPException(
                    status_code=400,
                    detail=str(exc)
                ) from exc
        elif mode == "poisson":
            try:
                prediction_data = predict_with_poisson(match_data)
            except FileNotFoundError as exc:
                raise HTTPException(
                    status_code=400,
                    detail=str(exc)
                ) from exc
        else:
            try:
                prediction_data = predict_with_ensemble(match_data)
            except FileNotFoundError as exc:
                raise HTTPException(
                    status_code=400,
                    detail=str(exc)
                ) from exc

        recomendacion = prediction_data["recomendacion"]
        explicacion = prediction_data["motivo"]
        probabilidades = prediction_data.get("probabilidades")

        if mode == "classic":
            prompt = f"""
Eres Aquinielator, un asistente que explica predicciones de quiniela.

Partido:
Local: {partido.local}
Visitante: {partido.visitante}

Datos del análisis:
- Recomendación calculada: {prediction_data['recomendacion']}
- Motivo base: {prediction_data['motivo']}

Responde exactamente en este formato:

Recomendacion: {prediction_data['recomendacion']}
Explicacion: explicación breve en español

No añadas nada más.
"""
        else:
            prompt = f"""
Eres Aquinielator, un asistente que explica predicciones de quiniela.

Partido:
Local: {partido.local}
Visitante: {partido.visitante}

Predicción del modelo {mode.upper()}:
- Recomendación calculada: {prediction_data['recomendacion']}
- Probabilidad 1: {probabilidades['1']}
- Probabilidad X: {probabilidades['X']}
- Probabilidad 2: {probabilidades['2']}
- Motivo base: {prediction_data['motivo']}

Responde exactamente en este formato:

Recomendacion: {prediction_data['recomendacion']}
Explicacion: explicación breve en español

No añadas nada más.
"""

        try:
            respuesta_llm = ask_ollama(prompt)

            lineas = respuesta_llm.splitlines()
            for linea in lineas:
                if linea.lower().startswith("recomendacion:"):
                    valor = linea.split(":", 1)[1].strip()
                    if valor in ["1", "X", "2"]:
                        recomendacion = valor
                elif linea.lower().startswith("explicacion:"):
                    explicacion = linea.split(":", 1)[1].strip()

        except Exception:
            explicacion = prediction_data["motivo"]

        resultados.append(
            MatchPrediction(
                local=partido.local,
                visitante=partido.visitante,
                recomendacion=recomendacion,
                explicacion=explicacion,
                probabilidades=probabilidades
            )
        )

    return QuinielaResponse(resultado=resultados)
