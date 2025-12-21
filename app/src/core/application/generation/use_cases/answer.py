from typing import List, Tuple

from src.core.application.generation.schemas.answer import LLMRequest, LLMResponse
from src.core.domain.document import CoreDocument, ExtendedVectorisedDocument, VectorisedDocument
from src.infra.adapters.embeddings import EmbedderInterface
from src.infra.adapters.llm import LLMInterface
from src.infra.adapters.preprocessing.llm_preprocessor import LLMPreprocessor
from src.infra.adapters.prompts.jinjaPrompter import CaseEnum
from src.infra.adapters.rerank import RerankerInterface
from src.infra.adapters.vdb import VectorDBInterface


class AnswerUC:
    def __init__(
        self,
        vdb_gateway: VectorDBInterface,
        embedder: EmbedderInterface,
        llm_adapter: LLMPreprocessor,
        reranker: RerankerInterface,
        llm: LLMInterface
    ):
        self._vdb_gateway = vdb_gateway
        self._embedder = embedder
        self._llm_adapter = llm_adapter
        self._reranker = reranker
        self._llm = llm

    async def execute(self, request: LLMRequest) -> Tuple[LLMResponse,
                                                          List[CoreDocument]]:
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
            top_k=5)

        documents: List[CoreDocument] = [
            CoreDocument(text=doc.text, metadata=doc.metadata)
            for doc in relevant_documents.value]

        context = "\n\n".join([doc.text for doc in documents])

        query_with_context = CoreDocument(
            text=summarised_query.text,
            metadata={"context": context}
        )

        summarised_query_with_context: CoreDocument = await self._llm_adapter.preprocess(
            document=query_with_context, case=CaseEnum.generate_answer, model=request.model
        )

        llm_response: LLMResponse = await self._llm.get_answer(
            model=request.model,
            query=summarised_query_with_context.text
        )

        return (llm_response, documents)
