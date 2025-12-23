from dishka import Provider, Scope, provide

from src.core.application.searching.use_cases.search import SearchUC
from src.infra.adapters.embeddings import FridaEmbedder
from src.infra.adapters.preprocessing.llm_preprocessor import LLMPreprocessor
from src.infra.adapters.rerank import BGEReranker
from src.infra.adapters.vdb import QdrantGateway


class SearchUCProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_search_uc(
        self,
        vdb_gateway: QdrantGateway,
        embedder: FridaEmbedder,
        llm_adapter: LLMPreprocessor,
        reranker: BGEReranker,
    ) -> SearchUC:
        return SearchUC(vdb_gateway=vdb_gateway, embedder=embedder,
                        llm_adapter=llm_adapter, reranker=reranker)
