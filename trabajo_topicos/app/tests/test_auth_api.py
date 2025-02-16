import pytest
from httpx import AsyncClient

BASE_URL = "http://localhost:8010"

@pytest.mark.asyncio
async def test_valid_api_key():
    """Verifica que una API Key válida permite acceder a los servicios con arrays."""
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/service/", headers={"Authorization": "freemium-key"}, json={
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

@pytest.mark.asyncio
async def test_invalid_api_key():
    """Verifica que una API Key inválida devuelve error 403."""
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/service/", headers={"Authorization": "invalid-key"}, json={
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
        assert response.status_code == 403
        assert response.json() == {"detail": "Invalid API Key"}
