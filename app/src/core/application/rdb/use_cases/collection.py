from typing import List
from uuid import UUID

from src.core.application.rdb.schemas.collection import (
    CollectionResponse,
    CreateCollectionRequest,
    UpdateCollectionRequest,
)
from src.core.domain.rdb_entities import DocumentCollection


class GetAvailableCollectionsUC:
    def __init__(self, rdb_repo):
        self.rdb_repo = rdb_repo

    async def execute(self, user_id: UUID) -> List[CollectionResponse]:
        collections = await self.rdb_repo.get_available_collections(user_id)
        return [CollectionResponse(**c.model_dump()) for c in collections]


class CreateCollectionUC:
    def __init__(self, rdb_repo):
        self.rdb_repo = rdb_repo

    async def execute(self, request: CreateCollectionRequest, user_id: UUID) -> CollectionResponse:
        if await self.rdb_repo.collection_exists(request.name, user_id):
            raise ValueError(
                f"Collection with name '{request.name}' already exists")
        collection = await self.rdb_repo.create_collection(request, user_id)
        return CollectionResponse(**collection.model_dump())


class UpdateCollectionUC:
    def __init__(self, rdb_repo):
        self.rdb_repo = rdb_repo

    async def execute(
            self, request: UpdateCollectionRequest, user_id: UUID) -> None:
        collection = await self.rdb_repo.get_collection_by_id(request.collection_id)
        if not collection or (collection.owner_id !=
                              user_id and not collection.is_public):
            raise ValueError("Collection not found or access denied")
        await self.rdb_repo.update_collection(request)


class DeleteCollectionUC:
    def __init__(self, rdb_repo):
        self.rdb_repo = rdb_repo

    async def execute(self, collection_id: UUID, user_id: UUID) -> None:
        collection = await self.rdb_repo.get_collection_by_id(collection_id)
        if not collection:
            raise ValueError("Collection not found")
        if collection.owner_id != user_id:
            raise ValueError("Access denied")
        await self.rdb_repo.delete_collection(collection_id)


class GetCollectionUC:
    def __init__(self, rdb_repo):
        self.rdb_repo = rdb_repo

    async def execute(
            self, collection_id: UUID, user_id: UUID) -> CollectionResponse:
        collection = await self.rdb_repo.get_collection_by_id(collection_id)
        if not collection or (collection.owner_id !=
                              user_id and not collection.is_public):
            raise ValueError("Collection not found or access denied")
        return CollectionResponse(**collection.model_dump())
