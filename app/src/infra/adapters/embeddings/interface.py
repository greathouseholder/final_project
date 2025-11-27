from abc import ABC, abstractmethod
from result import Result

from src.core.domain.document import CoreDocument, VectorisedDocument


class EmbedderInterface(ABC):
    @abstractmethod
    def embed(self, text: str) -> Result[list[float], str]: ...

    @abstractmethod
    def embed_document(self, document: CoreDocument) -> Result[VectorisedDocument, str]: ...