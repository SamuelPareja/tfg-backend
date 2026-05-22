"""
Tests básicos del endpoint /api/teams.
"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_teams_endpoint():
    """
    Comprueba que el endpoint /api/teams devuelve equipos desde MySQL.
    """
    response = client.get("/api/teams")

    assert response.status_code == 200

    data = response.json()

    assert "equipos" in data
    assert "equipos_detalle" in data
    assert len(data["equipos"]) >= 20