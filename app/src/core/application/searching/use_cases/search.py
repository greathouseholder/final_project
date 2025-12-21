from typing import List

from src.core.application.searching.schemas.search import SearchRequest
from src.core.domain.document import CoreDocument, ExtendedVectorisedDocument, VectorisedDocument
from src.infra.adapters.embeddings import EmbedderInterface
from src.infra.adapters.preprocessing.llm_preprocessor import LLMPreprocessor
from src.infra.adapters.prompts.jinjaPrompter import CaseEnum
from src.infra.adapters.rerank import RerankerInterface
from src.infra.adapters.vdb import VectorDBInterface


class SearchUC:
    def __init__(
        self,
        vdb_gateway: VectorDBInterface,
        embedder: EmbedderInterface,
        llm_adapter: LLMPreprocessor,
        reranker: RerankerInterface,
    ):
        self._vdb_gateway = vdb_gateway
        self._embedder = embedder
        self._llm_adapter = llm_adapter
        self._reranker = reranker

    async def execute(self, request: SearchRequest) -> list[CoreDocument]:
        query = CoreDocument(text=request.query, metadata={})

        summarised_query: CoreDocument = await self._llm_adapter.preprocess(
            document=query, case=CaseEnum.preprocess_query, model=request.model
        )

        embedded_query: VectorisedDocument = self._embedder.embed_document(
            summarised_query).value

        relevant_documents: List[ExtendedVectorisedDocument] = await self._vdb_gateway.search(
            embedding=embedded_query.embedding, collection_name=request.collection_name
        )

        relevant_documents: List[VectorisedDocument] = self._reranker.rerank(
            query=summarised_query, documents=relevant_documents,
            top_k=request.top_k)

        return [
            CoreDocument(text=doc.text, metadata=doc.metadata) for doc in relevant_documents.value
        ]
