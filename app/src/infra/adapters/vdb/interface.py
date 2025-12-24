# src/core/infra/adapters/vdb/interface.py
from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from result import Result

from src.core.domain.document import VectorisedDocument, ExtendedVectorisedDocument


class VectorDBInterface(ABC):
    """
    Абстрактный интерфейс для работы с векторной базой данных.
    Все реализации (Qdrant и потенциально другие) должны следовать этому контракту.
    """

    @abstractmethod
    async def create_collection(
        self,
        collection_id: UUID,
        vector_size: int,
        distance: str = "Cosine",
    ) -> Result[str, str]:
        """
        Создаёт коллекцию в векторной БД.
        В Qdrant имя коллекции = str(collection_id)
        """
        ...

    @abstractmethod
    async def delete_collection(
        self,
        collection_id: UUID,
    ) -> Result[str, str]:
        """Удаляет коллекцию и все её точки"""
        ...

    @abstractmethod
    async def add(
        self,
        document: VectorisedDocument,
        collection_id: UUID,
        document_id: UUID,
        chunk_index: int | None = None,
    ) -> Result[str, str]:
        """
        Добавляет один чанк в векторную базу.
        Возвращает ID созданной точки или ошибку.
        """
        ...

    @abstractmethod
    async def bulk_add(
        self,
        documents: List[VectorisedDocument],
        collection_id: UUID,
        document_id: UUID,
    ) -> Result[List[str], str]:
        """
        Массово добавляет чанки одного документа.
        Возвращает список ID точек или ошибку.
        """
        ...

    @abstractmethod
    async def search(
        self,
        embedding: List[float],
        collection_id: UUID,
        limit: int = 30,
        score_threshold: float | None = None,
    ) -> List[ExtendedVectorisedDocument]:
        """
        Выполняет поиск по вектору строго внутри одной коллекции.
        Фильтрация по collection_id обязательна на уровне реализации.
        """
        ...