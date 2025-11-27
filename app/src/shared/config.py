import os

from dotenv import load_dotenv
from dataclasses import dataclass


load_dotenv()


@dataclass
class Config:
    LLM_API_KEY: str = os.getenv("LLM_API_KEY")
    ALLOW_ORIGINS: str = os.getenv("ALLOW_ORIGINS", "*")
    ALLOW_CREDENTIALS: str = os.getenv("ALLOW_CREDENTIALS", "*")
    ALLOW_METHODS: str = os.getenv("ALLOW_METHODS", "*")
    ALLOW_HEADERS: str = os.getenv("ALLOW_HEADERS", "*")

    APP_CORS_ORIGINS_LIST = os.getenv('APP_CORS_ORIGINS_LIST', default='').split(',')
    APP_NGINX_PREFIX: str = os.getenv('APP_NGINX_PREFIX', default='/')


config = Config()
