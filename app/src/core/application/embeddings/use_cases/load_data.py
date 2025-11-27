from typing import Any

from result import Result

from src.core.application.embeddings.schemas.load_data import LoadDataRequest
from src.infra.adapters.chunks import ChunkAdapterInterface
from src.infra.adapters.embeddings import EmbedderInterface
from src.infra.adapters.vdb import VectorDBInterface


class LoadingUC:
    __slots__ = ('_vdb_gateway', '_embedder', '_chunk_adapter')

    def __init__(
            self,
            vdb_gateway: VectorDBInterface,
            embedder: EmbedderInterface,
            chunk_adapter: ChunkAdapterInterface
    ):
        self._vdb_gateway = vdb_gateway
        self._embedder = embedder
        self._chunk_adapter = chunk_adapter

    async def execute(self, request: LoadDataRequest) -> Result[str, Any]:
        split_document = self._chunk_adapter.split(
            text=request.data,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap
        )
        embedded_chunks = [
            self._embedder.embed_document(document).value for document in split_document
        ]
        for batch_index in range(0, len(embedded_chunks), 100):
            await self._vdb_gateway.bulk_add(
                embedded_chunks[batch_index:batch_index+100],
                collection_name=request.collection_name
            )
