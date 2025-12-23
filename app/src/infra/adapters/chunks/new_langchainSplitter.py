from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.core.domain.document import CoreDocument
from src.infra.adapters.chunks import ChunkAdapterInterface


class LangChainSplitter(ChunkAdapterInterface):
    def __init__(self, chunk_size: int = 300, chunk_overlap: int = 100):
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            add_start_index=True,
        )

    @staticmethod
    def to_langchain(document: CoreDocument):
        return Document(
            page_content=document.text,
            metadata=document.metadata
        )

    @staticmethod
    def from_langchain(document: Document):
        return CoreDocument(
            text=document.page_content,
            metadata=document.metadata
        )

    def split(self, text: CoreDocument) -> list[CoreDocument]:
        document = self.to_langchain(text)
        chunks = self._text_splitter.split_documents([document])
        return [self.from_langchain(chunk) for chunk in chunks]
