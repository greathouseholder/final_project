from dishka import Provider, Scope, provide
from qdrant_client import AsyncQdrantClient

from src.shared.config import config
from src.core.application.searching.use_cases.search import SearchUC
from src.infra.adapters.embeddings import FridaEmbedder
from src.infra.adapters.preprocessing.llm_preprocessor import LLMPreprocessor
from src.infra.adapters.rerank import BGEReranker
from src.infra.adapters.vdb import QdrantGateway


class SearchProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_qdrant_client(self) -> AsyncQdrantClient:
        return AsyncQdrantClient(
            url=config.qdrant_url,
            api_key=config.QDRANT_API_KEY,
        )

    @provide(scope=Scope.APP)
    def provide_qdrant_gateway(self, client: AsyncQdrantClient) -> QdrantGateway:
        return QdrantGateway(client)

    @provide(scope=Scope.APP)
    def provide_frida_embedder(self) -> FridaEmbedder:
        return FridaEmbedder()

    @provide(scope=Scope.APP)
    def provide_llm_preprocessor(self) -> LLMPreprocessor:
        return LLMPreprocessor()

    @provide(scope=Scope.APP)
    def provide_bge_reranker(self) -> BGEReranker:
        return BGEReranker()

    @provide(scope=Scope.REQUEST)
    def provide_search_uc(
        self,
        vdb: QdrantGateway,
        embedder: FridaEmbedder,
        llm_adapter: LLMPreprocessor,
        reranker: BGEReranker,
    ) -> SearchUC:
        return SearchUC(vdb_gateway=vdb, embedder=embedder,
                        llm_adapter=llm_adapter, reranker=reranker)