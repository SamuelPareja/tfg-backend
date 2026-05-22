"""
Tests básicos del endpoint /api/info.
"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_info_endpoint():
    """
    Comprueba que el endpoint /api/info responde correctamente.
    """
    response = client.get("/api/info")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == "Aquinielator API"
    assert data["framework"] == "FastAPI"
    assert data["database"] == "MySQL"