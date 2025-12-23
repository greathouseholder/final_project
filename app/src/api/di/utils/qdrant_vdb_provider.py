from dishka import Provider, Scope, provide
from qdrant_client import AsyncQdrantClient

from src.infra.adapters.vdb.interface import VectorDBInterface
from src.infra.adapters.vdb.qdrantGateway import QdrantGateway
from src.shared.config import config


class QdrantProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_async_qdrant_client(self) -> AsyncQdrantClient:
        return AsyncQdrantClient(
            url="http://localhost:6333", # хз
            api_key=None,
        )

    @provide(scope=Scope.APP)
    def provide_qdrant_gateway(
            self, client: AsyncQdrantClient) -> VectorDBInterface:
        return QdrantGateway(client)
