from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
import pymongo.errors
import os
import traceback

# URL de MongoDB (desde variable de entorno o predeterminada)
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

async def verify_api_key(api_key: str):
    try:
        # Conectar a MongoDB solo durante la llamada
        client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=5000)
        db = client.graph_db

        await client.server_info()  # Verificar la conexión con MongoDB

        # Verificar si la API Key existe en la base de datos
        user = await db.api_keys.find_one({"api_key": api_key})
        if not user:
            raise HTTPException(status_code=403, detail="Invalid API Key")

        return user

    except HTTPException as http_exc:
        print(f"⚠️ HTTPException: {http_exc.detail}")
        raise http_exc

    except pymongo.errors.ServerSelectionTimeoutError as db_error:
        print(f"Database connection error: {db_error}")
        raise HTTPException(status_code=503, detail="Database unavailable")

    except Exception as e:
        error_trace = traceback.format_exc()
        print(f" Unexpected Error:\n{error_trace}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    finally:
        # Cerrar la conexión después de cada solicitud
        client.close()
