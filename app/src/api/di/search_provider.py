from dishka import Provider, Scope, provide

from src.core.application.searching.use_cases.search import SearchUC
from src.infra.adapters.embeddings import Frida
from src.infra.adapters.preprocessing.llm_preprocessor import LLMPreprocessor
from src.infra.adapters.rerank import RerankerInterface
from src.infra.adapters.vdb import VectorDBInterface


class SearchProvider(Provider):

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
