import pytest
from httpx import AsyncClient

BASE_URL = "http://localhost:8010"

@pytest.mark.asyncio
async def test_freemium_rate_limit():
    """Verifica que el límite de 5 RPM para FREEMIUM se aplica correctamente."""
    async with AsyncClient(base_url=BASE_URL) as client:
        for _ in range(5):
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

        # La sexta solicitud debe fallar
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
        assert response.status_code == 429
        assert response.json() == {"detail": "Rate limit exceeded"}
