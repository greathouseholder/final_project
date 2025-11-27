from src.core.application.searching.schemas.search import SearchRequest
from src.core.domain.document import CoreDocument
from src.infra.adapters.embeddings import EmbedderInterface
from src.infra.adapters.preprocessing.llm_preprocessor import LLMPreprocessor
from src.infra.adapters.promts.jinjaPrompter import CaseEnum
from src.infra.adapters.rerank import RerankerInterface
from src.infra.adapters.vdb import VectorDBInterface


class SearchUC:
    def __init__(
            self,
            vdb_gateway: VectorDBInterface,
            embedder: EmbedderInterface,
            llm_adapter: LLMPreprocessor,
            reranker: RerankerInterface
    ):
        self._vdb_gateway = vdb_gateway
        self._embedder = embedder
        self._llm_adapter = llm_adapter
        self._reranker = reranker

    async def execute(self, request: SearchRequest) -> list[CoreDocument]:
        query = CoreDocument(
            text=request.query,
            metadata={}
        )
        summarised_query = await self._llm_adapter.preprocess(
            document=query,
            case=CaseEnum.preprocess_query,
            model=request.model
        )
        embedded_query = self._embedder.embed_document(summarised_query).value

        relevant_documents = await self._vdb_gateway.search(
            embedding=embedded_query.embedding,
            collection_name=request.collection_name
        )

        relevant_documents = self._reranker.rerank(
            query=summarised_query,
            documents=relevant_documents,
            top_k=5
        )

        return [
            CoreDocument(
                text=doc.text,
                metadata=doc.metadata
            ) for doc in relevant_documents.value
        ]



