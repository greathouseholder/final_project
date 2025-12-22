from typing import List
from uuid import UUID

from src.core.application.rdb.schemas.document import DocumentResponse, UpdateDocumentRequest
from src.core.domain.rdb_entities import Document


class GetAvailableDocumentsUC:
    def __init__(self, rdb_repo):
        self.rdb_repo = rdb_repo

    async def execute(
            self, collection_id: UUID, user_id: UUID) -> List[DocumentResponse]:
        collection = await self.rdb_repo.get_collection_by_id(collection_id)
        if not collection:
            raise FileNotFoundError("Collection not found")
        if collection.owner_id != user_id and not collection.is_public:
            raise PermissionError("Access denied")
        docs = await self.rdb_repo.get_documents_in_collection(collection_id)
        return [DocumentResponse(**d.model_dump()) for d in docs]


class UpdateDocumentUC:
    def __init__(self, rdb_repo):
        self.rdb_repo = rdb_repo

    async def execute(
            self, request: UpdateDocumentRequest, user_id: UUID) -> None:
        doc = await self.rdb_repo.get_document_by_id(request.document_id)
        if not doc:
            raise FileNotFoundError("Document not found")
        collection = await self.rdb_repo.get_collection_by_id(doc.collection_id)
        if collection.owner_id != user_id:
            raise PermissionError("Access denied")
        await self.rdb_repo.update_document(request)


class DeleteDocumentUC:
    def __init__(self, rdb_repo):
        self.rdb_repo = rdb_repo

    async def execute(self, document_id: UUID, user_id: UUID) -> None:
        doc = await self.rdb_repo.get_document_by_id(document_id)
        if not doc:
            raise FileNotFoundError("Document not found")
        collection = await self.rdb_repo.get_collection_by_id(doc.collection_id)
        if collection.owner_id != user_id:
            raise PermissionError("Access denied")
        await self.rdb_repo.delete_document(document_id)


class GetDocumentUC:
    def __init__(self, rdb_repo):
        self.rdb_repo = rdb_repo

    async def execute(
            self, document_id: UUID, user_id: UUID) -> DocumentResponse:
        doc = await self.rdb_repo.get_document_by_id(document_id)
        if not doc:
            raise FileNotFoundError("Document not found")
        collection = await self.rdb_repo.get_collection_by_id(doc.collection_id)
        if collection.owner_id != user_id and not collection.is_public:
            raise PermissionError("Access denied")
        return DocumentResponse(**doc.model_dump())
