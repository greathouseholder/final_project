import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.api import container, routers

# from src.api.di import container


app = FastAPI(title="RAG Telegram Bot for Lawyers API")

app.include_router(routers)


@app.get("/health")
async def health_check():
    """Проверка работоспособности сервиса"""
    return {"status": "ok"}


setup_dishka(container, app)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
