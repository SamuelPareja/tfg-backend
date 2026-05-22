from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class MatchInput(BaseModel):
    local: str = Field(..., example="Real Madrid")
    visitante: str = Field(..., example="FC Barcelona")


class QuinielaRequest(BaseModel):
    partidos: List[MatchInput]


class MatchPrediction(BaseModel):
    local: str
    visitante: str
    recomendacion: str
    explicacion: str
    probabilidades: Optional[Dict[str, float]] = None


class QuinielaResponse(BaseModel):
    resultado: List[MatchPrediction]