from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CreateCollectionRequest(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False


class UpdateCollectionRequest(BaseModel):
    collection_id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None


class CollectionResponse(BaseModel):
    collection_id: UUID
    name: str
    description: Optional[str]
    document_count: int
    is_public: bool
