import uvicorn

from fastapi import FastAPI
from src.api.v1.routers import routers


app = FastAPI(
    title="RAG Telegram Bot for Lawyers API"
)

app.include_router(routers)


@app.get("/health")
async def health_check():
    """Проверка работоспособности сервиса"""
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
