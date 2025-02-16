import aioredis
from fastapi import HTTPException
import os

# Conexión a Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6380")
redis = aioredis.from_url(REDIS_URL, decode_responses=True)

# Configuración de límites
RATE_LIMITS = {
    "FREEMIUM": 5,   # 5 solicitudes por minuto
    "PREMIUM": 50    # 50 solicitudes por minuto
}

async def rate_limiter(user):
    subscription = user.get("subscription", "FREEMIUM")
    limit = RATE_LIMITS.get(subscription, 5)

    key = f"rate_limit:{user['api_key']}"

    # Incrementar el contador en Redis
    current_count = await redis.incr(key)

    if current_count == 1:
        # Establecer el tiempo de expiración del contador (60 segundos)
        await redis.expire(key, 60)

    if current_count > limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
