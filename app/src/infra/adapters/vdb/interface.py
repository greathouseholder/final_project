from typing import List
from result import Result
from abc import ABC, abstractmethod

from src.core.domain.document import VectorisedDocument, ExtendedVectorisedDocument


class VectorDBInterface(ABC):

    @abstractmethod
    async def create_collection(self, collection_name: str = 'alpha', **kwargs) -> Result[str, str]: ...

    @abstractmethod
    async def add(self, document: VectorisedDocument, collection_name: str = 'alpha') -> Result[str, str]: ...

    @abstractmethod
    async def search(self, embedding: list[float], collection_name: str = 'alpha') -> List[ExtendedVectorisedDocument]: ...

    @abstractmethod
    async def bulk_add(self, documents: List[VectorisedDocument], collection_name: str = 'alpha') -> Result[str, str]: ...