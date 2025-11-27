import asyncio
from qdrant_client import models
from qdrant_client.models import Distance

from scripts.load_data import convert_to_documents, loading
from scripts.frames import websites
from scripts.my_collections import create_specific_collection, delete_specific_collection
from scripts.searching_baseline import mark_all_questions
from src.infra.adapters.embeddings.bge import BGEEmbedder

bge_config = models.VectorParams(size=1024, distance=Distance.COSINE)
collection = 'baseline'
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"


async def baseline_embedding():
    await create_specific_collection(collection_name=collection, vectors_config=bge_config)
    docs = convert_to_documents(websites)
    await loading(docs, BGEEmbedder(), collection, chunk_size=400, chunk_overlap=100)


async def main():
    await baseline_embedding()
    await mark_all_questions(collection)


async def deleting():
    await delete_specific_collection(collection_name=collection)


if __name__ == '__main__':
    asyncio.run(main())
