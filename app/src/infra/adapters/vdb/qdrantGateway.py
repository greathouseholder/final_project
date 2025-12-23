import uuid
from typing import List
from uuid import UUID

from qdrant_client import AsyncQdrantClient, models
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from result import Err, Ok, Result

from src.core.domain.document import ExtendedVectorisedDocument, VectorisedDocument
from src.core.infra.adapters.vdb.interface import VectorDBInterface


class QdrantGateway(VectorDBInterface):
    __slots__ = ("_client",)

    def __init__(self, client: AsyncQdrantClient):
        self._client = client

    @staticmethod
    def _build_payload(
        document: VectorisedDocument,
        collection_id: str,
        document_id: str,
        chunk_index: int | None = None,
    ) -> dict:
        """Формирует payload для точки в Qdrant"""
        payload = {
            "text": document.text,
            "collection_id": collection_id,
            "document_id": document_id,
        }
        if chunk_index is not None:
            payload["chunk_index"] = chunk_index

        if hasattr(document, "metadata") and document.metadata:
            payload["metadata"] = document.metadata

        return payload

    async def add(
        self,
        document: VectorisedDocument,
        collection_id: UUID,
        document_id: UUID,
        chunk_index: int | None = None,
    ) -> Result[str, str]:
        point_id = str(uuid.uuid4())

        res = await self._client.upsert(
            collection_name=str(collection_id),
            points=[
                models.PointStruct(
                    id=point_id,
                    vector=document.embedding,
                    payload=self._build_payload(
                        document=document,
                        collection_id=str(collection_id),
                        document_id=str(document_id),
                        chunk_index=chunk_index,
                    ),
                )
            ],
        )

        return Ok(point_id) if res.status == models.UpdateStatus.COMPLETED else Err(str(res))

    async def bulk_add(
        self,
        documents: List[VectorisedDocument],
        collection_id: UUID,
        document_id: UUID,
    ) -> Result[List[str], str]:
        points = []
        point_ids = []

        for idx, doc in enumerate(documents):
            point_id = str(uuid.uuid4())
            point_ids.append(point_id)
            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=doc.embedding,
                    payload=self._build_payload(
                        document=doc,
                        collection_id=str(collection_id),
                        document_id=str(document_id),
                        chunk_index=idx,
                    ),
                )
            )

        res = await self._client.upsert(
            collection_name=str(collection_id),
            points=points,
        )

        return Ok(point_ids) if res.status == models.UpdateStatus.COMPLETED else Err(str(res))

    async def search(
        self,
        embedding: List[float],
        collection_id: UUID,
        limit: int = 30,
        score_threshold: float | None = None,
    ) -> List[ExtendedVectorisedDocument]:
        search_params = {
            "collection_name": str(collection_id),
            "query_vector": embedding,
            "limit": limit,
            "with_vectors": True,
            "with_payload": True,
        }

        filter_ = Filter(
            must=[
                FieldCondition(
                    key="collection_id",
                    match=MatchValue(value=str(collection_id)),
                )
            ]
        )
        search_params["query_filter"] = filter_

        if score_threshold is not None:
            search_params["score_threshold"] = score_threshold

        response = await self._client.search(**search_params)

        results = []
        for res in response:
            payload = res.payload or {}
            results.append(
                ExtendedVectorisedDocument(
                    text=payload.get("text", ""),
                    metadata=payload.get("metadata", {}),
                    embedding=res.vector or [],
                    id=res.id,
                    distance=res.score,
                )
            )

        return results

    async def create_collection(
        self,
        collection_id: UUID,
        vector_size: int,
        distance: models.Distance = models.Distance.COSINE,
    ) -> Result[str, str]:
        try:
            await self._client.create_collection(
                collection_name=str(collection_id),
                vectors_config=models.VectorParams(size=vector_size, distance=distance),
            )
            return Ok("Collection created successfully")
        except Exception as e:
            return Err(str(e))

    async def delete_collection(self, collection_id: UUID) -> Result[str, str]:
        try:
            await self._client.delete_collection(collection_name=str(collection_id))
            return Ok("Collection deleted successfully")
        except Exception as e:
            return Err(str(e))