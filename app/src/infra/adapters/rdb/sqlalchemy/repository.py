from typing import List, Optional
from uuid import UUID

from app.src.core.application.rdb.schemas.collection import (
    CreateCollectionRequest,
    UpdateCollectionRequest,
)
from app.src.core.application.rdb.schemas.document import UpdateDocumentRequest
from app.src.core.domain.rdb_entities import Document, DocumentCollection, User
from app.src.infra.adapters.rdb.interface import RDBRepository
from app.src.infra.adapters.rdb.sqlalchemy.models import CollectionModel, DocumentModel, UserModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyRDBRepository(RDBRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return User.model_validate(model.__dict__) if model else None

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.user_id == user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return User.model_validate(model.__dict__) if model else None

    async def create_user(self, telegram_id: int, role: str = "user") -> User:
        model = UserModel(telegram_id=telegram_id, role=role)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return User.model_validate(model.__dict__)

    async def collection_exists(self, name: str, owner_id: UUID) -> bool:
        stmt = select(CollectionModel).where(
            CollectionModel.name == name,
            CollectionModel.owner_id == owner_id
        )
        result = await self.session.execute(stmt)
        return bool(result.scalar_one_or_none())

    async def create_collection(self, request: CreateCollectionRequest, owner_id: UUID) -> DocumentCollection:
        model = CollectionModel(
            name=request.name,
            description=request.description,
            owner_id=owner_id,
            is_public=request.is_public
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return DocumentCollection.model_validate(model.__dict__)

    async def get_available_collections(self, user_id: UUID) -> List[DocumentCollection]:
        stmt = select(CollectionModel).where(
            (CollectionModel.owner_id == user_id) | (CollectionModel.is_public == True)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [DocumentCollection.model_validate(m.__dict__) for m in models]

    async def get_collection_by_id(self, collection_id: UUID) -> Optional[DocumentCollection]:
        stmt = select(CollectionModel).where(CollectionModel.collection_id == collection_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return DocumentCollection.model_validate(model.__dict__) if model else None

    async def update_collection(self, request: UpdateCollectionRequest) -> None:
        stmt = update(CollectionModel).where(CollectionModel.collection_id == request.collection_id).values(
            name=request.name if request.name is not None else CollectionModel.name,
            description=request.description if request.description is not None else CollectionModel.description,
            is_public=request.is_public if request.is_public is not None else CollectionModel.is_public
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_collection(self, collection_id: UUID) -> None:
        stmt = delete(CollectionModel).where(CollectionModel.collection_id == collection_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_documents_in_collection(self, collection_id: UUID) -> List[Document]:
        stmt = select(DocumentModel).where(DocumentModel.collection_id == collection_id)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [Document.model_validate(m.__dict__) for m in models]

    async def get_document_by_id(self, document_id: UUID) -> Optional[Document]:
        stmt = select(DocumentModel).where(DocumentModel.document_id == document_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return Document.model_validate(model.__dict__) if model else None

    async def create_document(self, collection_id: UUID, title: str, description: str | None, file_name: str, file_size: int, metadata: dict) -> Document:
        model = DocumentModel(
            collection_id=collection_id,
            title=title,
            description=description,
            file_name=file_name,
            file_size=file_size,
            metadata=metadata
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return Document.model_validate(model.__dict__)

    async def update_document(self, request: UpdateDocumentRequest) -> None:
        stmt = update(DocumentModel).where(DocumentModel.document_id == request.document_id).values(
            title=request.title if request.title is not None else DocumentModel.title,
            description=request.description if request.description is not None else DocumentModel.description,
            metadata=request.metadata if request.metadata is not None else DocumentModel.metadata
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_document(self, document_id: UUID) -> None:
        stmt = delete(DocumentModel).where(DocumentModel.document_id == document_id)
        await self.session.execute(stmt)
        await self.session.commit()