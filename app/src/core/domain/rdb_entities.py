from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class User(BaseModel):
    """Бизнес-сущность пользователя (из RDB)"""
    user_id: UUID = Field(..., description="UUID пользователя")
    telegram_id: int = Field(..., description="Telegram ID")
    created_at: datetime = Field(..., description="Дата создания")
    role: str = Field(..., description="Роль: 'user' или 'admin'")
    is_paid: bool = False
    attempt_count: int = 0


class DocumentCollection(BaseModel):
    """Бизнес-сущность коллекции документов"""
    collection_id: UUID = Field(..., description="UUID коллекции (используется в Qdrant)")
    name: str = Field(..., description="Название коллекции")
    description: Optional[str] = Field(None, description="Описание")
    document_count: int = Field(0, description="Количество документов")
    owner_id: UUID = Field(..., description="UUID владельца (user_id)")
    is_public: bool = Field(False, description="Доступна ли всем пользователям")
    created_at: datetime = Field(..., description="Дата создания")


class Document(BaseModel):
    """Бизнес-сущность документа (метаданные, хранятся в RDB)"""
    document_id: UUID = Field(..., description="UUID документа")
    collection_id: UUID = Field(..., description="UUID коллекции")
    title: str = Field(..., description="Название документа")
    description: Optional[str] = Field(None, description="Описание")
    file_name: str = Field(..., description="Оригинальное имя файла")
    file_size: int = Field(..., description="Размер в байтах")
    created_at: datetime = Field(..., description="Дата создания")
    path: Optional[str] = Field(None, description="Путь к файлу на диске (если нужно)")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Метаданные документа")