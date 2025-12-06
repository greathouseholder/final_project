from dishka import Provider, Scope, provide

from src.core.application.embeddings.use_cases.load_data import LoadDataUC
from src.infra.adapters.chunks import LangChainSplitter
from src.infra.adapters.embeddings import Frida
from src.infra.adapters.vdb import QdrantGateway


class LoadDataProvider(Provider):

    @provide(scope=Scope.APP)
    def provide_load_data_uc(
        self,
        vdb_gateway: QdrantGateway,
        embedder: Frida,
        chunk_adapter: LangChainSplitter
    ) -> LoadDataUC:
        return LoadDataUC(
            vdb_gateway=vdb_gateway,
            embedder=embedder,
            chunk_adapter=chunk_adapter
        )
