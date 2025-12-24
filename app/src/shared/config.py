import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()

def _parse_cors_origins() -> list[str]:
    value = os.getenv("APP_CORS_ORIGINS_LIST", "")
    return [origin.strip() for origin in value.split(",") if origin.strip()]

@dataclass
class Config:
    GIGACHAT_CREDENTIALS: str = os.getenv("GIGACHAT_CREDENTIALS", "")
    GIGACHAT_SCOPE: str = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")

    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
    QDRANT_API_KEY: str | None = os.getenv("QDRANT_API_KEY")  # None для локального Qdrant

    @property
    def qdrant_url(self) -> str:
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "app")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "rag_db")

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    ALLOW_ORIGINS: str = os.getenv("ALLOW_ORIGINS", "*")
    ALLOW_CREDENTIALS: str = os.getenv("ALLOW_CREDENTIALS", "true")
    ALLOW_METHODS: str = os.getenv("ALLOW_METHODS", "*")
    ALLOW_HEADERS: str = os.getenv("ALLOW_HEADERS", "*")

    APP_CORS_ORIGINS_LIST: list[str] = field(default_factory=_parse_cors_origins)
    APP_NGINX_PREFIX: str = os.getenv("APP_NGINX_PREFIX", "/")


config = Config()