import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from src.api import container, log_request, routers
from sqlalchemy.ext.asyncio import create_async_engine
from src.shared.config import config
from src.infra.adapters.rdb.sqlalchemy.models import Base

engine = create_async_engine(config.RELATIONAL_DATABASE_URL, echo=False)

app = FastAPI(title="RAG Telegram Bot for Lawyers API")


@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(routers)


@app.middleware("http")
async def middleware(request, call_next):
    return await log_request(request, call_next)


@app.get("/health")
async def is_alive():
    return {"success": "ok"}

setup_dishka(container, app)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
