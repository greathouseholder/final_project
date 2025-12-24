from unittest.mock import MagicMock
import pytest
from langchain_core.documents import Document as LCDocument

from src.core.domain.document import CoreDocument
from src.infra.adapters.chunks.new_langchainSplitter import NewLangChainSplitter
from src.infra.adapters.chunks.langchainSplitter import LangChainSplitter
from src.infra.adapters.documents.langchain import LangchainAdapter


@pytest.fixture
def long_text_document():
    text = "Word " * 100
    return CoreDocument(text=text, metadata={"source": "test"})


class TestNewLangChainSplitter:
    def test_conversion_methods(self):
        core_doc = CoreDocument(text="test", metadata={"a": 1})
        lc_doc = NewLangChainSplitter.to_langchain(core_doc)
        assert isinstance(lc_doc, LCDocument)
        assert lc_doc.page_content == "test"
        assert lc_doc.metadata == {"a": 1}
        new_core_doc = NewLangChainSplitter.from_langchain(lc_doc)
        assert isinstance(new_core_doc, CoreDocument)
        assert new_core_doc.text == "test"
        assert new_core_doc.metadata == {"a": 1}

    def test_split_logic(self, long_text_document):
        splitter = NewLangChainSplitter(chunk_size=100, chunk_overlap=10)
        chunks = splitter.split(long_text_document)
        assert isinstance(chunks, list)
        assert len(chunks) > 1
        assert all(isinstance(chunk, CoreDocument) for chunk in chunks)
        assert chunks[0].metadata["source"] == "test"
        assert "start_index" in chunks[0].metadata


class TestLangChainSplitter:
    def test_split_delegation(self, long_text_document):
        mock_adapter = MagicMock(spec=LangchainAdapter)
        lc_doc = LCDocument(page_content=long_text_document.text, metadata=long_text_document.metadata)
        mock_adapter.to_langchain.return_value = lc_doc
        def side_effect_from_langchain(doc):
            return CoreDocument(text=doc.page_content, metadata=doc.metadata)
        mock_adapter.from_langchain.side_effect = side_effect_from_langchain
        splitter = LangChainSplitter(langchain_adapter=mock_adapter)
        chunks = splitter.split(long_text_document, chunk_size=100, chunk_overlap=10)

        assert mock_adapter.to_langchain.called
        assert mock_adapter.from_langchain.called
        assert len(chunks) > 1
        assert isinstance(chunks[0], CoreDocument)