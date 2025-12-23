import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.api import container, log_request, routers

app = FastAPI(title="RAG Telegram Bot for Lawyers API")

app.include_router(routers)


@app.middleware("http")
async def middleware(request, call_next):
    return await log_request(request, call_next)


@app.get("health")
async def is_alive():
    return {"success": "ok"}

setup_dishka(container, app)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
