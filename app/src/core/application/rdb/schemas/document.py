from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class UpdateDocumentRequest(BaseModel):
    document_id: UUID
    title: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class DocumentResponse(BaseModel):
    document_id: UUID
    collection_id: UUID
    title: str
    description: Optional[str]
    file_name: str
    file_size: int
    created_at: datetime = Field(description="Дата создания")
    payload: Dict[str, Any]