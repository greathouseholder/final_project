import uvicorn

from fastapi import FastAPI
from src.api.v1.routers import router


app = FastAPI(
    title="RAG Telegram Bot for Lawyers API"
)

app.include_router(router)


@app.get("/health")
async def health_check():
    """Проверка работоспособности сервиса"""
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
