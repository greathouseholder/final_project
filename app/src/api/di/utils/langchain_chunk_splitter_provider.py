from dishka import Provider, Scope, provide

from src.infra.adapters.chunks.interface import ChunkAdapterInterface
from src.infra.adapters.chunks.new_langchainSplitter import NewLangChainSplitter


class LangChainProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_langchain_splitter(
            self,) -> ChunkAdapterInterface:
        return NewLangChainSplitter()
