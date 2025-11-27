from abc import ABC, abstractmethod

from src.core.domain.document import CoreDocument


class ChunkAdapterInterface(ABC):
    @abstractmethod
    def split(self, text: CoreDocument, **kwargs) -> list[CoreDocument]: ...
