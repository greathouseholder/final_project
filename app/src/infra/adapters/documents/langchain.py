from src.core.domain.document import CoreDocument
from langchain_core.documents import Document

class LangchainAdapter:
    @staticmethod
    def to_langchain(document: CoreDocument) -> Document:
        return Document(
            page_content=document.text,
            metadata=document.metadata
        )

    @staticmethod
    def from_langchain(document: Document) -> CoreDocument:
        return CoreDocument(
            text=document.page_content,
            metadata=document.metadata
        )