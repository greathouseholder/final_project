from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.core.application.rdb.schemas.collection import (
    CreateCollectionRequest,
    UpdateCollectionRequest,
)
from src.core.application.rdb.schemas.document import UpdateDocumentRequest
from src.core.domain.rdb_entities import Document, DocumentCollection, User


class RDBRepository(ABC):

    @abstractmethod
    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    async def create_user(self, telegram_id: int, role: str = "user") -> User:
        pass

    @abstractmethod
    async def collection_exists(self, name: str, owner_id: UUID) -> bool:
        pass

    @abstractmethod
    async def create_collection(self, request: CreateCollectionRequest, owner_id: UUID) -> DocumentCollection:
        pass

    @abstractmethod
    async def get_available_collections(self, user_id: UUID) -> List[DocumentCollection]:
        pass

    @abstractmethod
    async def get_collection_by_id(self, collection_id: UUID) -> Optional[DocumentCollection]:
        pass

    @abstractmethod
    async def update_collection(self, request: UpdateCollectionRequest) -> None:
        pass

    @abstractmethod
    async def delete_collection(self, collection_id: UUID) -> None:
        pass

    @abstractmethod
    async def get_documents_in_collection(self, collection_id: UUID) -> List[Document]:
        pass

    @abstractmethod
    async def get_document_by_id(self, document_id: UUID) -> Optional[Document]:
        pass

    @abstractmethod
    async def create_document(self, collection_id: UUID, title: str, description: str | None, file_name: str, file_size: int, metadata: dict) -> Document:
        pass

    @abstractmethod
    async def update_document(self, request: UpdateDocumentRequest) -> None:
        pass

    @abstractmethod
    async def delete_document(self, document_id: UUID) -> None:
        pass