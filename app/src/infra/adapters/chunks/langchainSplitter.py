from src.core.domain.document import CoreDocument
from src.infra.adapters.chunks import ChunkAdapterInterface
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.infra.adapters.documents.langchain import LangchainAdapter


class LangChainSplitter(ChunkAdapterInterface):
    def __init__(
            self,
            langchain_adapter: LangchainAdapter
    ):
        self._langchain_adapter = langchain_adapter

    def split(
            self,
            text: CoreDocument,
            chunk_size=300,
            chunk_overlap=100
    ) -> list[CoreDocument]:
        document = self._langchain_adapter.to_langchain(text)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents([document])
        chunks = [self._langchain_adapter.from_langchain(chunk) for chunk in chunks]
        return chunks