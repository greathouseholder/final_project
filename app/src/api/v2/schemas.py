from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl


class CollectionShort(BaseModel):
    collection_id: int
    name: str
    description: Optional[str] = None

class Collection(BaseModel):
    collection_id: int
    name: str
    description: Optional[str] = None
    document_count: int
    is_public: bool
    created_at: Optional[datetime]

class DocumentShort(BaseModel):
    document_id: int
    collection_id: int
    title: str

class Document(BaseModel):
    document_id: int
    collection_id: int
    title: str
    file_name: str
    file_size: float
    created_at: Optional[datetime]
    metadata: Dict[str, Any] # тут возможны 'url' и 'relevance'

class ConversationShort(BaseModel):
    conversation_id: int
    collection_id: int
    name: str

class Message(BaseModel):
    message_id: int
    conversation_id: int
    content: str
    role: str
    sources: List[Document]

# Request schemas
class CollectionCreate(BaseModel):
    telegram_id: int = Field(..., description="Telegram ID пользователя")
    name: str = Field(..., min_length=1, max_length=255, description="Название коллекции")
    description: Optional[str] = Field(None, max_length=1000, description="Описание коллекции")
    is_public: bool = Field(None, description="Параметр публичности")

class CollectionUpdate(BaseModel):
    telegram_id: int = Field(..., description="Telegram ID пользователя")
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Новое название")
    description: Optional[str] = Field(None, max_length=1000, description="Новое описание")

class DocumentCreate(BaseModel):
    telegram_id: int = Field(..., description="Telegram ID пользователя")
    title: str = Field(..., min_length=1, max_length=255, description="Название документа")
    url: Optional[HttpUrl] = Field(None, description="URL источника документа")

class DocumentUpdate(BaseModel):
    telegram_id: int = Field(..., description="Telegram ID пользователя")
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Новое название")

class ConversationCreate(BaseModel):
    telegram_id: int = Field(..., description="Telegram ID пользователя")
    name: str = Field(..., min_length=1, max_length=255, description="Название диалога")
    collection_id: int = Field(..., description="ID коллекции")

class ConversationUpdate(BaseModel):
    telegram_id: int = Field(..., description="Telegram ID пользователя")
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Новое название")

class QueryRequest(BaseModel):
    telegram_id: int = Field(..., description="Telegram ID пользователя")
    query_text: str = Field(..., min_length=1, description="Текст запроса")

class SearchRequest(BaseModel):
    telegram_id: int = Field(..., description="Telegram ID пользователя")
    collection_id: int = Field(..., description="ID коллекции")
    number: int = Field(3, ge=1, le=10, description="Количество результатов")
    query_text: str = Field(..., min_length=1, description="Текст поискового запроса")
