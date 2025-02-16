from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.services.auth_api import verify_api_key
from app.services.rate_limiter_api import rate_limiter
from app.services.logger_api import log_request
from app.routes.similarity_api import router as similarity_router
import traceback

app = FastAPI()

@app.middleware("http")
async def log_middleware(request: Request, call_next):
    response = await log_request(request, call_next)
    return response

@app.middleware("http")
async def auth_and_rate_limit_middleware(request: Request, call_next):
    try:
        api_key = request.headers.get("Authorization")

        if not api_key:
            raise HTTPException(status_code=401, detail="API Key missing")

        user = await verify_api_key(api_key)
        await rate_limiter(user)

        response = await call_next(request)
        return response

    except HTTPException as http_exc:
        return JSONResponse(status_code=http_exc.status_code, content={"detail": http_exc.detail})

    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Internal Server Error:\n{error_trace}")
        return JSONResponse(status_code=500, content={"detail": f"Internal Server Error", "trace": error_trace})

# Registrar el router del modelo
app.include_router(similarity_router, prefix="/service")

@app.get("/")
async def root():
    return {"message": "La API se está ejecutando"}
