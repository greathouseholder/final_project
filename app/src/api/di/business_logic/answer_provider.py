from dishka import Provider, Scope, provide

from src.core.application.generation.use_cases.answer import AnswerUC
from src.infra.adapters.embeddings.frida import FridaEmbedder
from src.infra.adapters.llm.gigachatGenerator import GigaChatClient
from src.infra.adapters.preprocessing.llm_preprocessor import LLMPreprocessor
from src.infra.adapters.rerank.bge_reranker import BGEReranker
from src.infra.adapters.vdb.qdrantGateway import QdrantGateway


class AnswerUCProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_answer_uc(
            self,
            vdb_gateway: QdrantGateway,
            embedder: FridaEmbedder,
            llm_adapter: LLMPreprocessor,
            reranker: BGEReranker,
            llm: GigaChatClient) -> AnswerUC:
        return AnswerUC(
            vdb_gateway,
            embedder,
            llm_adapter,
            reranker,
            llm
        )
