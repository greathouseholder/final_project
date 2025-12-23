import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    GIGACHAT_CREDENTIALS: str = os.getenv("GIGACHAT_CREDENTIALS")
    GIGACHAT_SCOPE: str = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")

    LLM_API_KEY: str = os.getenv("LLM_API_KEY")
    ALLOW_ORIGINS: str = os.getenv("ALLOW_ORIGINS", "*")
    ALLOW_CREDENTIALS: str = os.getenv("ALLOW_CREDENTIALS", "*")
    ALLOW_METHODS: str = os.getenv("ALLOW_METHODS", "*")
    ALLOW_HEADERS: str = os.getenv("ALLOW_HEADERS", "*")

    APP_CORS_ORIGINS_LIST = os.getenv(
        "APP_CORS_ORIGINS_LIST", default="").split(",")
    APP_NGINX_PREFIX: str = os.getenv("APP_NGINX_PREFIX", default="/")

    RELATIONAL_DATABASE_URL: str = ...


config = Config()
