import os
from dishka import Provider, Scope, provide
from src.core.application.searching.use_cases.search import SearchUC
from src.infra.adapters.embeddings import Frida
from src.infra.adapters.preprocessing.llm_preprocessor import LLMPreprocessor
from src.infra.adapters.rerank import RerankerInterface
from src.infra.adapters.rerank.bge_reranker import BGEReranker
from src.infra.adapters.vdb.qdrantGateway import QdrantGateway
from src.infra.adapters.vdb import VectorDBInterface

class SearchProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_vdb(self) -> VectorDBInterface:
        host = os.getenv("QDRANT_HOST", "qdrant")
        port = int(os.getenv("QDRANT_PORT", 6333))
        return QdrantGateway(host=host, port=port)
    @provide(scope=Scope.APP)
    def provide_frida(self) -> Frida:
        return Frida()
    @provide(scope=Scope.APP)
    def provide_reranker(self) -> RerankerInterface:
        return BGEReranker()
    @provide(scope=Scope.APP)
    def provide_llm_preprocessor(self) -> LLMPreprocessor:
        return LLMPreprocessor()
    @provide(scope=Scope.APP)
    def provide_search_uc(
        self,
        vdb: VectorDBInterface,
        embedder: Frida,
        llm_adapter: LLMPreprocessor,
        reranker: RerankerInterface,
    ) -> SearchUC:
        return SearchUC(
            vdb_gateway=vdb,
            embedder=embedder,
            llm_adapter=llm_adapter,
            reranker=reranker
        )