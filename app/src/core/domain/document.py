from typing import Any

from pydantic import BaseModel


class CoreDocument(BaseModel):
    """Сущность живет только до этапа векторизации"""
    text: str
    metadata: dict[str, Any]


class VectorisedDocument(CoreDocument):
    """Векторизованный документ"""
    embedding: list[float]


class ExtendedVectorisedDocument(VectorisedDocument):
    """Векторизованный документ, который достали из векторной базы данных"""
    id: str
    distance: float

# TO-DO: переписать, т.к. нельзя в domain использовать pydantic
