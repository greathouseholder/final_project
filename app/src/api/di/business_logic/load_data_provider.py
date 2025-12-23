from dishka import Provider, Scope, provide

from src.core.application.embeddings.use_cases.load_data import LoadingUC
from src.infra.adapters.chunks import LangChainSplitter
from src.infra.adapters.embeddings import FridaEmbedder
from src.infra.adapters.vdb import QdrantGateway


class LoadDataProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_langchain_splitter(self) -> LangChainSplitter:
        return LangChainSplitter(  # можно настраивать по идее
            chunk_size=500,
            chunk_overlap=50,
        )

    # @provide(scope=Scope.APP)
    # def provide_frida_embedder(self) -> FridaEmbedder:
    #     return FridaEmbedder()

    @provide(scope=Scope.APP)
    def provide_load_data_uc(
        self,
        vdb_gateway: QdrantGateway,
        embedder: FridaEmbedder,
        chunk_adapter: LangChainSplitter
    ) -> LoadingUC:
        return LoadingUC(
            vdb_gateway=vdb_gateway, embedder=embedder,
            chunk_adapter=chunk_adapter)
