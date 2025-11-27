from qdrant_client import AsyncQdrantClient

from src.infra.adapters.vdb.qdrantGateway import QdrantGateway

vdb = QdrantGateway(client=AsyncQdrantClient(host='localhost', port=6333))

async def create_specific_collection(collection_name: str, **kwargs):
    await vdb.create_collection(collection_name=collection_name, **kwargs)

async def delete_specific_collection(collection_name: str):
    await vdb.delete_collection(collection_name=collection_name)
