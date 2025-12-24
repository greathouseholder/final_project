from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class CollectionShort(BaseModel):
    collection_id: UUID
    name: str
    description: Optional[str] = None


class Collection(BaseModel):
    collection_id: UUID
    name: str
    description: Optional[str] = None
    document_count: int
    is_public: bool
    created_at: Optional[datetime]


class DocumentShort(BaseModel):
    document_id: UUID
    collection_id: UUID
    title: str


class Document(BaseModel):
    document_id: UUID
    collection_id: UUID
    description: Optional[str] = None
    title: str
    file_name: str
    file_size: float
    created_at: Optional[datetime]
    metadata: Dict[str, Any]


# Request schemas

class BaseRequest(BaseModel):
    telegram_id: int


class UploadDocumentRequest(BaseRequest):
    title: str = Field(..., min_length=1, max_length=255,
                       description="Название документа")
    description: Optional[str] = Field(
        None, max_length=1000, description="Описание документа")
    url: Optional[HttpUrl] = Field(None, description="URL источника документа")


class CollectionCreate(BaseRequest):
    name: str = Field(..., min_length=1, max_length=255,
                      description="Название коллекции")
    description: Optional[str] = Field(
        None, max_length=1000, description="Описание коллекции")
    is_public: bool = Field(default=False, description="Параметр публичности")


class CollectionUpdate(BaseRequest):
    name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Новое название")
    description: Optional[str] = Field(
        None, max_length=1000, description="Новое описание")
    is_public: Optional[bool] = Field(
        None, description="Публичность коллекции")


class DocumentCreate(BaseRequest):
    title: str = Field(..., min_length=1, max_length=255,
                       description="Название документа")
    url: Optional[HttpUrl] = Field(None, description="URL источника документа")


class DocumentUpdate(BaseRequest):
    title: Optional[str] = Field(
        None, min_length=1, max_length=255, description="Новое название")
    description: Optional[str] = Field(
        None, max_length=1000, description="Новое описание")


class QueryRequest(BaseRequest):
    query_text: str = Field(..., min_length=1, description="Текст запроса")


class SearchRequest(BaseRequest):
    collection_id: UUID = Field(..., description="ID коллекции")
    number: int = Field(3, ge=1, le=10, description="Количество результатов")
    query_text: str = Field(..., min_length=1,
                            description="Текст поискового запроса")
