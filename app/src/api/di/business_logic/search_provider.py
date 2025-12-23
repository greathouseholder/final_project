from dishka import Provider, Scope, provide

from src.core.application.searching.use_cases.search import SearchUC
from src.infra.adapters.embeddings.interface import EmbedderInterface
from src.infra.adapters.preprocessing.interface import Preprocessor
from src.infra.adapters.rerank.interface import RerankerInterface
from src.infra.adapters.vdb.interface import VectorDBInterface


class SearchUCProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_search_uc(
        self,
        vdb_gateway: VectorDBInterface,
        embedder: EmbedderInterface,
        llm_adapter: Preprocessor,
        reranker: RerankerInterface,
    ) -> SearchUC:
        return SearchUC(vdb_gateway=vdb_gateway, embedder=embedder,
                        llm_adapter=llm_adapter, reranker=reranker)
