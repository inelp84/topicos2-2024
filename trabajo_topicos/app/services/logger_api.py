import logging
import time
from fastapi import Request

# Configuración del logger
logger = logging.getLogger("graph_similarity_api")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

async def log_request(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(f"{request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.4f}s")
    return response