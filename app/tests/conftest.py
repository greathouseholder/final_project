import pytest
from unittest.mock import AsyncMock, MagicMock
from result import Ok

from src.core.domain.document import (
    CoreDocument,
    VectorisedDocument,
    ExtendedVectorisedDocument,
)
from src.core.application.generation.schemas.answer import LLMResponse
from src.infra.adapters.embeddings.interface import EmbedderInterface
from src.infra.adapters.vdb.interface import VectorDBInterface
from src.infra.adapters.llm.interface import LLMInterface
from src.infra.adapters.rerank.interface import RerankerInterface
from src.infra.adapters.preprocessing.interface import Preprocessor
from src.infra.adapters.prompts.jinjaPrompter import JinjaPrompter
from src.infra.adapters.validation.interface import ValidatorInterface

@pytest.fixture
def sample_core_document() -> CoreDocument:
    """Базовый CoreDocument для тестов"""
    return CoreDocument(
        text="Это тестовый документ о машинном обучении.",
        metadata={"source": "test", "page": 1}
    )

@pytest.fixture
def sample_vectorised_document() -> VectorisedDocument:
    """VectorisedDocument с фейковым эмбеддингом"""
    return VectorisedDocument(
        text="Тестовый векторизованный документ.",
        metadata={"source": "test"},
        embedding=[0.1] * 1024
    )

@pytest.fixture
def sample_extended_document() -> ExtendedVectorisedDocument:
    """ExtendedVectorisedDocument из 'БД'"""
    return ExtendedVectorisedDocument(
        text="Документ из векторной базы.",
        metadata={
            "title": "Test Title",
            "kind": "article",
            "web_id": "123",
            "url": "https://example.com"
        },
        embedding=[0.1] * 1024,
        id="test-uuid-123",
        distance=0.95
    )

@pytest.fixture
def sample_extended_documents(sample_extended_document) -> list[ExtendedVectorisedDocument]:
    """Список документов для тестирования поиска/реранкинга"""
    docs = []
    for i in range(5):
        doc = ExtendedVectorisedDocument(
            text=f"Документ номер {i} о различных темах.",
            metadata={
                "title": f"Title {i}",
                "kind": "article",
                "web_id": str(i),
                "url": f"https://example.com/{i}"
            },
            embedding=[0.1 * (i + 1)] * 1024,
            id=f"uuid-{i}",
            distance=0.9 - (i * 0.1)
        )
        docs.append(doc)
    return docs


@pytest.fixture
def mock_embedder() -> MagicMock:
    """Мок EmbedderInterface"""
    embedder = MagicMock(spec=EmbedderInterface)
    def embed_document_side_effect(document: CoreDocument):
        return Ok(VectorisedDocument(
            text=document.text,
            metadata=document.metadata,
            embedding=[0.1] * 1024
        ))
    embedder.embed.return_value = Ok([0.1] * 1024)
    embedder.embed_document.side_effect = embed_document_side_effect
    return embedder

@pytest.fixture
def mock_vdb_gateway() -> AsyncMock:
    """Мок VectorDBInterface"""
    gateway = AsyncMock(spec=VectorDBInterface)
    gateway.create_collection.return_value = Ok("success")
    gateway.add.return_value = Ok("success")
    gateway.bulk_add.return_value = Ok("success")
    gateway.search.return_value = []
    return gateway


@pytest.fixture
def mock_llm() -> AsyncMock:
    """Мок LLMInterface"""
    llm = AsyncMock(spec=LLMInterface)
    llm.get_answer.return_value = LLMResponse(
        model="test-model",
        response_text="Тестовый ответ от LLM"
    )
    llm.generate.return_value = LLMResponse(
        model="test-model",
        response_text="Тестовый ответ"
    )
    return llm

@pytest.fixture
def mock_reranker(sample_extended_documents) -> MagicMock:
    """Мок RerankerInterface"""
    reranker = MagicMock(spec=RerankerInterface)
    reranked = sample_extended_documents[:3]
    for i, doc in enumerate(reranked):
        doc.metadata["rerank_score"] = 0.9 - (i * 0.1)
    reranker.rerank.return_value = Ok(reranked)
    return reranker


@pytest.fixture
def mock_validator() -> AsyncMock:
    """Мок ValidatorInterface"""
    validator = AsyncMock(spec=ValidatorInterface)
    async def validate_side_effect(response: LLMResponse, document: CoreDocument):
        return CoreDocument(
            text=response.response_text,
            metadata=document.metadata
        )
    validator.validate.side_effect = validate_side_effect
    return validator

@pytest.fixture
def mock_prompter() -> AsyncMock:
    """Мок JinjaPrompter"""
    prompter = AsyncMock(spec=JinjaPrompter)
    prompter.get_prompt.return_value = "Сгенерированный промпт: {query}"
    return prompter

@pytest.fixture
def mock_llm_preprocessor(mock_llm, mock_prompter, mock_validator) -> AsyncMock:
    """Мок LLMPreprocessor"""
    preprocessor = AsyncMock(spec=Preprocessor)
    async def preprocess_side_effect(document: CoreDocument, **kwargs):
        return CoreDocument(
            text=f"Обработанный: {document.text}",
            metadata=document.metadata
        )
    preprocessor.preprocess.side_effect = preprocess_side_effect
    return preprocessor
