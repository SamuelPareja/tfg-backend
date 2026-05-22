"""
Tests básicos del endpoint /health.
"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    """
    Comprueba que el endpoint /health responde correctamente.
    """
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["project"] == "Aquinielator API"