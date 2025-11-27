import uuid
from typing import List
from result import Result, Ok, Err
from qdrant_client import AsyncQdrantClient, models

from src.core.domain.document import VectorisedDocument, ExtendedVectorisedDocument
from src.infra.adapters.vdb import VectorDBInterface


class QdrantGateway(VectorDBInterface):
    __slots__ = ("_client", )

    def __init__(self, client: AsyncQdrantClient):
        self._client = client

    @staticmethod
    def get_payload(document: VectorisedDocument) -> dict:
        payload = document.metadata
        payload['text'] = document.text
        return payload

    async def add(
            self,
            document: VectorisedDocument,
            collection_name: str = 'baseline'
    ) -> Result[str, str]:
        res = await self._client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    payload=self.get_payload(document),
                    vector=document.embedding
                ),
            ],
        )

        return Ok(res) if res.status == 'completed' else Err(res)

    async def bulk_add(
            self,
            documents: list[VectorisedDocument],
            collection_name: str = 'baseline'
    ) -> Result[str, str]:
        res = await self._client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    payload=self.get_payload(document),
                    vector=document.embedding
                )
                for document in documents
            ],
        )

        return Ok(res) if res.status == 'completed' else Err(res)

    async def search(
            self,
            embedding: list[float],
            collection_name: str = 'baseline'
    ) -> List[ExtendedVectorisedDocument]:
        response = await self._client.search(
            collection_name=collection_name,
            query_vector=embedding,
            limit=30,
            with_vectors=True
        )
        return [
            ExtendedVectorisedDocument(
                text=res.payload['text'],
                metadata={
                    "title": res.payload.get('title'),
                    "kind": res.payload['kind'],
                    "web_id": res.payload['web_id'],
                    "url": res.payload['url'],
                },
                embedding=res.vector,
                id=res.id,
                distance=res.score,
            )
            for res in response
        ]

    async def create_collection(self, collection_name: str = 'baseline', **kwargs) -> Result[str, str]:
        await self._client.create_collection(
            collection_name=collection_name,
            **kwargs
        )
        return Ok('success')

    async def delete_collection(self, collection_name: str = 'baseline') -> Result[str, str]:
        await self._client.delete_collection(collection_name=collection_name)
        return Ok('success')