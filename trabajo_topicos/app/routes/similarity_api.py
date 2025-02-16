from fastapi import APIRouter, HTTPException, Request
from app.models.ml_model import run_similarity_model  # Importar el modelo de ML

router = APIRouter()

@router.post("/")
async def detect_similarity(request: Request):
    try:
        data = await request.json()
        inputs = data.get("inputs")

        if not inputs or len(inputs) != 2:
            raise HTTPException(status_code=400, detail="Se requieren exactamente dos subgrafos en 'inputs'.")

        result = run_similarity_model(inputs)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
