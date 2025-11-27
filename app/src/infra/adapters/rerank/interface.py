from abc import ABC, abstractmethod
from typing import List
from result import Result

from src.core.domain.document import VectorisedDocument


class RerankerInterface(ABC):
    @abstractmethod
    def rerank(
        self,
        query: str,
        documents: List[VectorisedDocument],
        top_k: int = 5
    ) -> Result[List[VectorisedDocument], str]:
        """
        Переранжирует список документов для запроса.
        Возвращает top_k документов, отсортированных по рейтингу релевантности (убыванию).
        Добавляет «rerank_score» (0-1) к метаданным каждого документа.
        """
        ...