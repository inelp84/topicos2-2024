import pytest
from httpx import AsyncClient
from app.main import app
from app.models.ml_model import run_similarity_model


BASE_URL = "http://localhost:8010"

@pytest.mark.asyncio
async def test_similarity_api():
    """Verifica que la API de similaridad responde correctamente con arrays."""
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/service/", headers={"Authorization": "premium-key"}, json={
            "inputs": [
                {
                    "nodes": [{"id": "A"}, {"id": "B"}],
                    "links": [{"source": "A", "target": "B"}]
                },
                {
                    "nodes": [{"id": "X"}, {"id": "Y"}],
                    "links": [{"source": "X", "target": "Y"}]
                }
            ]
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "probabilidad" in data
        assert isinstance(data["probabilidad"], float)
        assert 0 <= data["probabilidad"] <= 1

@pytest.mark.asyncio
async def test_similarity_api_invalid_input():
    """Verifica que la API devuelve error si los datos no están en formato de array."""
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/service/", headers={"Authorization": "premium-key"}, json={
            "inputs": ["Invalid Data"]
        })
        
        assert response.status_code == 400
        assert response.json() == {"detail": "Se requieren exactamente dos subgrafos en 'inputs'."}
