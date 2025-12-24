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
    QDRANT_API_KEY: str | None = os.getenv("QDRANT_API_KEY")

    @property
    def qdrant_url(self) -> str:
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

    ALLOW_ORIGINS: str = os.getenv("ALLOW_ORIGINS", "*")
    ALLOW_CREDENTIALS: str = os.getenv("ALLOW_CREDENTIALS", "true")
    ALLOW_METHODS: str = os.getenv("ALLOW_METHODS", "*")
    ALLOW_HEADERS: str = os.getenv("ALLOW_HEADERS", "*")

    APP_CORS_ORIGINS_LIST: list[str] = field(default_factory=_parse_cors_origins)
    APP_NGINX_PREFIX: str = os.getenv("APP_NGINX_PREFIX", "/")

    RELATIONAL_DATABASE_URL: str = os.getenv(
        "RELATIONAL_DATABASE_URL",
        "sqlite+aiosqlite:///./data/goodmanbase.db"
    )


config = Config()