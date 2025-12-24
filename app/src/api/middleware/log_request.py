import logging
import time
from logging.handlers import RotatingFileHandler

from fastapi import HTTPException, Request

logger = logging.getLogger("api")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = RotatingFileHandler(
    filename='src/shared/logs/api.log',
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
    encoding='utf-8'
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


async def log_request(request: Request, call_next):
    start_time = time.time()

    try:
        response = await call_next(request)
        duration = time.time() - start_time

        client_ip = request.client.host if request.client else "unknown"
        logger.info(
            f"{request.method} {request.url.path} - "
            f"status: {response.status_code} - "
            f"client: {client_ip} - "
            f"duration: {duration:.3f}s"
        )

        return response

    except HTTPException as http_exc:
        duration = time.time() - start_time
        client_ip = request.client.host if request.client else "unknown"
        logger.warning(
            f"{request.method} {request.url.path} - "
            f"status: {http_exc.status_code} - "
            f"client: {client_ip} - "
            f"duration: {duration:.3f}s - "
            f"detail: {http_exc.detail}"
        )
        raise

    except Exception as exc:
        duration = time.time() - start_time
        client_ip = request.client.host if request.client else "unknown"
        logger.error(
            f"{request.method} {request.url.path} - "
            f"status: 500 - "
            f"client: {client_ip} - "
            f"duration: {duration:.3f}s - "
            f"error: {type(exc).__name__}: {str(exc)}",
            exc_info=True
        )
        raise
