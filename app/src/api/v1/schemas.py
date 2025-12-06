"""
TODO: 
    1. Подумать, тут ли этот документ создан
    2. Поставить везде необходимые ограничения
    3. Уточнить про database_id
    4. Уточнить про relevance
"""
from typing import Annotated, Optional, List
from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, Field, PositiveInt, NonNegativeInt, AnyUrl, NonNegativeFloat


class Status(StrEnum):
    """Status value"""
    CREATED = "created"
    DELETED = "deleted"


class Request(BaseModel):
    # чему равна максимальная длина id в tg?
    user_id: PositiveInt = Field(ge=0)


class Document(BaseModel):
    title: str
    relevance: NonNegativeFloat = Field(ge=0.0)
    url: Optional[AnyUrl]


class RagRequest(Request):
    query_text: str = Field(min_length=1, max_length=250)
    database_id: str


class RagResponse(BaseModel):
    answer: str
    sources: List[Document]


class SearchRequest(Request):
    query_text: str = Field(min_length=1, max_length=250)
    database_id: str


class SearchResponse(BaseModel):
    documents: List[Document]


class Database(BaseModel):
    database_id: str
    name: str = Field(min_length=1, max_length=30)


class DatabaseGet(Database):
    document_count: NonNegativeInt
    created_at: datetime


class DatabasesGetResponse(BaseModel):
    databases: List[DatabaseGet]


class DatabaseCreateRequest(Request):
    name: str = Field(min_length=1, max_length=30)


class DatabaseCreateResponse(Database):
    status: Status
    created_at: datetime


class DatabaseDeleteResponse(Database):
    status: Status
    deleted_documents: NonNegativeInt
    deleted_at: datetime


class UploadErrorInfo(BaseModel):
    file: str
    reason: str


class DatabaseUploadResponse(BaseModel):
    database_id: str
    processed_files: NonNegativeInt
    failed_filed: NonNegativeInt
    errors: List[UploadErrorInfo]
    total_size_mb: NonNegativeFloat
