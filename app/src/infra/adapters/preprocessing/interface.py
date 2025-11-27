from abc import ABC, abstractmethod
from src.core.domain.document import CoreDocument

class Preprocessor(ABC):
    @abstractmethod
    async def preprocess(self, document: CoreDocument, **kwargs) -> CoreDocument:
        pass