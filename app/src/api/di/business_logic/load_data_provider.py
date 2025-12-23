from dishka import Provider, Scope, provide

from src.core.application.embeddings.use_cases.load_data import LoadingUC
from src.infra.adapters.chunks import LangChainSplitter
from src.infra.adapters.embeddings import FridaEmbedder
from src.infra.adapters.vdb import QdrantGateway


class LoadingUCProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_load_data_uc(
        self,
        vdb_gateway: QdrantGateway,
        embedder: FridaEmbedder,
        chunk_adapter: LangChainSplitter
    ) -> LoadingUC:
        return LoadingUC(
            vdb_gateway=vdb_gateway,
            embedder=embedder,
            chunk_adapter=chunk_adapter)
