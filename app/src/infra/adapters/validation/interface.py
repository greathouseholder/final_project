from abc import ABC, abstractmethod

from src.core.application.generation.schemas.answer import LLMResponse
from src.core.domain.document import CoreDocument


class ValidatorInterface(ABC):
    @abstractmethod
    async def validate(self, response: LLMResponse, document: CoreDocument) -> CoreDocument: ...