import pandas as pd
from src.core.domain.document import CoreDocument


def to_document(row: dict) -> CoreDocument:
    return CoreDocument(
        text=row["text"],
        metadata={
            'web_id': row["web_id"],
            'url': row["url"],
            'kind': row.get("kind", 'html'),
            'title': row["title"],
        }
    )

def convert_to_documents(data: pd.DataFrame) -> list[CoreDocument]:
    documents = []
    for index, row in data.iterrows():
        documents.append(to_document(row))

    return documents

from qdrant_client import AsyncQdrantClient

from src.core.application.embeddings.schemas.load_data import LoadDataRequest
from src.core.application.embeddings.use_cases.load_data import LoadingUC
from src.core.domain.document import CoreDocument
from src.infra.adapters.chunks.langchainSplitter import LangChainSplitter
from src.infra.adapters.documents.langchain import LangchainAdapter
from src.infra.adapters.vdb.qdrantGateway import QdrantGateway
from tqdm import tqdm


async def loading(
        docs: list[CoreDocument],
        embedder,
        collection_name: str = 'baseline',
        chunk_size: int = 300,
        chunk_overlap: int = 100,
):
    splitter = LangChainSplitter(LangchainAdapter())
    vdb = QdrantGateway(client=AsyncQdrantClient(host='localhost', port=6333))
    uc = LoadingUC(
        vdb_gateway=vdb,
        embedder=embedder,
        chunk_adapter=splitter,
    )
    for doc in tqdm(docs, desc="Загружаем документы в базу данных"):
        await uc.execute(LoadDataRequest(
            data=doc,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            collection_name=collection_name
        ))

