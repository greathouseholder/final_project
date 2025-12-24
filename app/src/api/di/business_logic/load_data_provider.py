from dishka import Provider, Scope, provide

from src.core.application.embeddings.use_cases.load_data import LoadingUC
from src.infra.adapters.chunks.interface import ChunkAdapterInterface
from src.infra.adapters.embeddings.interface import EmbedderInterface
from src.infra.adapters.vdb.interface import VectorDBInterface


class LoadingUCProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_load_data_uc(
        self,
        vdb_gateway: VectorDBInterface,
        embedder: EmbedderInterface,
        chunk_adapter: ChunkAdapterInterface
    ) -> LoadingUC:
        return LoadingUC(
            vdb_gateway=vdb_gateway,
            embedder=embedder,
            chunk_adapter=chunk_adapter)
