import importlib

import pytest


def _reload_config_module(monkeypatch, env: dict[str, str | None]):
    for key, value in env.items():
        if value is None:
            monkeypatch.delenv(key, raising=False)
        else:
            monkeypatch.setenv(key, value)

    mod = importlib.import_module("src.shared.config")
    return importlib.reload(mod)


def test_parse_cors_origins_list(monkeypatch):
    mod = _reload_config_module(
        monkeypatch,
        {
            "APP_CORS_ORIGINS_LIST": " https://a.com, http://b.com  , ,https://c.com,,   ",
        },
    )

    assert mod.config.APP_CORS_ORIGINS_LIST == [
        "https://a.com",
        "http://b.com",
        "https://c.com",
    ]


def test_qdrant_url_is_built_from_host_and_port(monkeypatch):
    mod = _reload_config_module(
        monkeypatch,
        {
            "QDRANT_HOST": "qdrant-service",
            "QDRANT_PORT": "7777",
        },
    )

    assert mod.config.QDRANT_HOST == "qdrant-service"
    assert mod.config.QDRANT_PORT == 7777
    assert mod.config.qdrant_url == "http://qdrant-service:7777"


def test_postgres_dsn_is_built(monkeypatch):
    mod = _reload_config_module(
        monkeypatch,
        {
            "POSTGRES_HOST": "db",
            "POSTGRES_PORT": "5433",
            "POSTGRES_USER": "user1",
            "POSTGRES_PASSWORD": "pass1",
            "POSTGRES_DB": "rag_db_test",
        },
    )

    assert mod.config.POSTGRES_HOST == "db"
    assert mod.config.POSTGRES_PORT == 5433
    assert mod.config.postgres_dsn == (
        "postgresql+asyncpg://user1:pass1@db:5433/rag_db_test"
    )


def test_qdrant_api_key_can_be_none(monkeypatch):
    mod = _reload_config_module(
        monkeypatch,
        {
            "QDRANT_API_KEY": None,
        },
    )
    assert mod.config.QDRANT_API_KEY is None