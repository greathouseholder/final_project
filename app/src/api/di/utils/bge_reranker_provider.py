from dishka import Provider, Scope, provide

from src.infra.adapters.rerank.bge_reranker import BGEReranker
from src.infra.adapters.rerank.interface import RerankerInterface


class BGERerankerProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_bge_reranker(self) -> RerankerInterface:
        return BGEReranker()
