from dishka import Provider, Scope, provide

from src.core.application.generation.use_cases.answer import AnswerUC
from src.infra.adapters.embeddings.interface import EmbedderInterface
from src.infra.adapters.llm.interface import LLMInterface
from src.infra.adapters.preprocessing.interface import Preprocessor
from src.infra.adapters.rerank.interface import RerankerInterface
from src.infra.adapters.vdb.interface import VectorDBInterface


class AnswerUCProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_answer_uc(
            self,
            vdb_gateway: VectorDBInterface,
            embedder: EmbedderInterface,
            llm_adapter: Preprocessor,
            reranker: RerankerInterface,
            llm: LLMInterface) -> AnswerUC:
        return AnswerUC(
            vdb_gateway,
            embedder,
            llm_adapter,
            reranker,
            llm
        )
