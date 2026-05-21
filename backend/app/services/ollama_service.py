import os
from groq import Groq


MODEL_NAME = "llama-3.3-70b-versatile"


def ask_ollama(prompt: str) -> str:
    """
    Mantengo el nombre ask_ollama para no romper el resto del proyecto,
    pero internamente ahora usa Groq en lugar de Ollama.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "No se ha encontrado la variable de entorno GROQ_API_KEY."
        )

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente que explica predicciones de quiniela. "
                    "No cambies la recomendación base salvo que ya venga dada. "
                    "Responde solo en el formato solicitado."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()