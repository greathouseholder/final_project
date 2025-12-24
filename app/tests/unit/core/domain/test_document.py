from __future__ import annotations

import dataclasses
from typing import Any

import pytest

from src.core.domain.document import CoreDocument, ExtendedVectorisedDocument, VectorisedDocument


def _dump(obj: Any) -> dict:
    """
    Универсальная "сериализация" без знания, dataclass это или pydantic.
    Так мы дергаем больше кода модели и делаем тест устойчивым.
    """
    if hasattr(obj, "model_dump"):  # pydantic v2
        return obj.model_dump()
    if hasattr(obj, "dict"):  # pydantic v1
        return obj.dict()
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    return dict(obj.__dict__)


def test_core_document_fields(sample_core_document: CoreDocument):
    assert sample_core_document.text
    assert isinstance(sample_core_document.metadata, dict)
    assert sample_core_document.metadata["source"] == "test"

    dumped = _dump(sample_core_document)
    assert dumped["text"] == sample_core_document.text
    assert dumped["metadata"]["page"] == 1


def test_vectorised_document_embedding(sample_vectorised_document: VectorisedDocument):
    assert sample_vectorised_document.text.startswith("Тестовый")
    assert isinstance(sample_vectorised_document.embedding, list)
    assert len(sample_vectorised_document.embedding) == 1024
    assert sample_vectorised_document.embedding[0] == pytest.approx(0.1)


def test_extended_vectorised_document_fields(sample_extended_document: ExtendedVectorisedDocument):
    assert sample_extended_document.id == "test-uuid-123"
    assert 0.0 <= sample_extended_document.distance <= 1.0

    md = sample_extended_document.metadata
    assert md["title"] == "Test Title"
    assert md["url"].startswith("https://")

    dumped = _dump(sample_extended_document)
    assert dumped["id"] == "test-uuid-123"
    assert "metadata" in dumped