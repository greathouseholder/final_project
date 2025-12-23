from app.src.infra.adapters.rdb.sqlalchemy.repository import SQLAlchemyRDBRepository
from dishka import Provider, Scope, provide
from qdrant_client import AsyncQdrantClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.adapters.embeddings import FridaEmbedder
from src.infra.adapters.preprocessing.llm_preprocessor import LLMPreprocessor
from src.infra.adapters.rerank import BGEReranker
from src.infra.adapters.vdb import QdrantGateway



class BGERerankerProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_bge_reranker(self) -> BGEReranker:
        return BGEReranker()
