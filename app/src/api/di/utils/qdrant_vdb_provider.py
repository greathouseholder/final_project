from dishka import Provider, Scope, provide
from qdrant_client import AsyncQdrantClient

from shared.config import config
from src.infra.adapters.vdb.qdrantGateway import QdrantGateway


class QdrantProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_async_qdrant_client(self) -> AsyncQdrantClient:
        return AsyncQdrantClient(
            url="http://localhost:6333", # хз
            api_key=None,
        )

    @provide(scope=Scope.APP)
    def provide_qdrant_gateway(
            self, client: AsyncQdrantClient) -> QdrantGateway:
        return QdrantGateway(client)
