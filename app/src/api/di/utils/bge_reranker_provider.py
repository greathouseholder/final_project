from dishka import Provider, Scope, provide

from src.infra.adapters.rerank.bge_reranker import BGEReranker


class BGERerankerProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_bge_reranker(self) -> BGEReranker:
        return BGEReranker()
