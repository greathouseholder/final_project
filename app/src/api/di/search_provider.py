from dishka import Provider, Scope, provide

from src.core.application.searching.use_cases.search import SearchUC
from src.infra.adapters.embeddings import Frida

# заменить LLMPreprocessor на конкретную реализацию
from src.infra.adapters.preprocessing.llm_preprocessor import LLMPreprocessor
from src.infra.adapters.rerank import BGEReranker
from src.infra.adapters.vdb import QdrantGateway


class SearchProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_search_uc(
        self,
        vdb: QdrantGateway,
        embedder: Frida,
        llm_adapter: LLMPreprocessor,
        reranker: BGEReranker,
    ) -> SearchUC:
        return SearchUC(vdb_gateway=vdb, embedder=embedder,
                        llm_adapter=llm_adapter, reranker=reranker)
