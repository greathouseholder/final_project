from abc import ABC, abstractmethod
from typing import List

from src.core.application.generation.schemas.answer import LLMResponse, Message


class LLMInterface(ABC):
    @abstractmethod
    async def generate(self, model: str, history: List[Message]) -> LLMResponse:
        pass

    @abstractmethod
    async def get_answer(self, model: str, query: str) -> LLMResponse:
        pass
