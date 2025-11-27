import asyncio
from qdrant_client import models
from qdrant_client.models import Distance

from scripts.load_data import convert_to_documents, loading
from scripts.frames import websites
from scripts.my_collections import delete_specific_collection, create_specific_collection
from src.infra.adapters.embeddings.bge import BGEEmbedder
from src.infra.adapters.embeddings.bert import BertEncoder


async def baseline_loading():
    # await create_specific_collection(
    #     collection_name='baseline',
    #     vectors_config=models.VectorParams(size=768, distance=Distance.COSINE)
    # )
    docs = convert_to_documents(websites)
    await loading(docs, BertEncoder(), 'baseline')
    # asyncio.run(delete_specific_collection('baseline'))

async def baseline_different_emb():
    # await create_specific_collection(
    #     collection_name='baseline_2',
    #     vectors_config=models.VectorParams(size=1024, distance=Distance.COSINE)
    # )
    docs = convert_to_documents(websites)
    await loading(docs, BGEEmbedder(), 'baseline_2', chunk_size=200, chunk_overlap=50)
    # asyncio.run(delete_specific_collection('baseline'))

bge_config = models.VectorParams(size=1024, distance=Distance.COSINE)

async def main():
    # await create_specific_collection(collection_name='baseline_3', vectors_config=bge_config)
    # await create_specific_collection(collection_name='baseline_4', vectors_config=bge_config)
    # await create_specific_collection(collection_name='baseline_5', vectors_config=bge_config)
    # await create_specific_collection(collection_name='baseline_6', vectors_config=bge_config)
    # await create_specific_collection(collection_name='baseline_7', vectors_config=bge_config)
    docs = convert_to_documents(websites)
    emb = BGEEmbedder()
    # await loading(docs, emb, 'baseline_3', chunk_size=200, chunk_overlap=50)
    # await loading(docs, emb, 'baseline_4', chunk_size=400, chunk_overlap=100)
    # await loading(docs, emb, 'baseline_5', chunk_size=400, chunk_overlap=50)
    # await loading(docs, emb, 'baseline_6', chunk_size=500, chunk_overlap=100)
    # await loading(docs, emb, 'baseline_7', chunk_size=200, chunk_overlap=100)

if __name__ == '__main__':
    asyncio.run(main())