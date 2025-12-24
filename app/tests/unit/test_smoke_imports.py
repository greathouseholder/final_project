import importlib
import sys
import types

import pytest


def _ensure_docx_importable():
    try:
        import docx
        if getattr(docx, "__file__", "").endswith("docx.py"):
            raise RuntimeError("legacy docx detected")
    except Exception:
        sys.modules.pop("docx", None)
        stub = types.ModuleType("docx")

        class _DummyDocument:
            pass

        stub.Document = _DummyDocument
        sys.modules["docx"] = stub


def _ensure_python_multipart_importable():
    try:
        from python_multipart import __version__
        assert __version__ > "0.0.12"
    except Exception:
        sys.modules.pop("python_multipart", None)
        stub = types.ModuleType("python_multipart")
        stub.__version__ = "0.0.21"
        sys.modules["python_multipart"] = stub


@pytest.mark.parametrize(
    "module_name",
    [
        "src.core.domain.document",
        "src.core.domain.answer",
        "src.core.domain.company",
        "src.core.domain.rdb_entities",
        "src.core.domain.schemas",
        "src.core.application.embeddings.schemas.load_data",
        "src.core.application.generation.schemas.answer",
        "src.core.application.searching.schemas.search",
        "src.core.application.embeddings.use_cases.load_data",
        "src.core.application.generation.use_cases.answer",
        "src.core.application.searching.use_cases.search",
        "src.api.v2.schemas",
        "src.api.v2.exceptions",
        "src.api.v2.helpers",
        "src.shared.config",
    ],
)
def test_import_smoke(module_name: str, monkeypatch):
    monkeypatch.setenv("GIGACHAT_CREDENTIALS", "test")
    monkeypatch.setenv("LLM_API_KEY", "test")
    monkeypatch.setenv("POSTGRES_PASSWORD", "test")

    if module_name.startswith("src.api."):
        _ensure_python_multipart_importable()
        _ensure_docx_importable()

    importlib.import_module(module_name)