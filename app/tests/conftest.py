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

from uuid import uuid4
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from dataclasses import dataclass

from src.core.domain.rdb_entities import User, Document, DocumentCollection
from src.core.application.embeddings.schemas.load_data import LoadDataRequest
from src.core.application.generation.schemas.answer import LLMRequest
from src.core.application.searching.schemas.search import SearchRequest
from src.core.application.rdb.schemas.collection import (
    CreateCollectionRequest,
    UpdateCollectionRequest,
    CollectionResponse,
)
from src.core.application.rdb.schemas.document import (
    UpdateDocumentRequest,
    DocumentResponse,
)
from src.infra.adapters.chunks.interface import ChunkAdapterInterface
from src.infra.adapters.rdb.interface import RDBRepository


@pytest.fixture
def sample_user_id():
    return uuid4()


@pytest.fixture
def sample_collection_id():
    return uuid4()


@pytest.fixture
def sample_document_id():
    return uuid4()


@pytest.fixture
def sample_user(sample_user_id):
    """Пользователь из RDB"""
    return User(
        user_id=sample_user_id,
        telegram_id=123456789,
        role="user",
        is_paid=False,
        attempt_count=5,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def sample_admin_user(sample_user_id):
    """Админ пользователь"""
    return User(
        user_id=sample_user_id,
        telegram_id=987654321,
        role="admin",
        is_paid=True,
        attempt_count=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def sample_collection(sample_collection_id, sample_user_id):
    """Коллекция из RDB"""
    return DocumentCollection(
        collection_id=sample_collection_id,
        name="Test Collection",
        description="Test Description",
        owner_id=sample_user_id,
        is_public=False,
        document_count=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def sample_public_collection(sample_collection_id, sample_user_id):
    """Публичная коллекция"""
    return DocumentCollection(
        collection_id=sample_collection_id,
        name="Public Collection",
        description="Public Description",
        owner_id=sample_user_id,
        is_public=True,
        document_count=5,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def sample_rdb_document(sample_document_id, sample_collection_id):
    """Документ из RDB"""
    return Document(
        document_id=sample_document_id,
        collection_id=sample_collection_id,
        title="Test Document",
        description="Test Description",
        file_name="test.pdf",
        file_size=1024,
        payload={"source": "test"},
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def mock_rdb_repo():
    """Мок RDBRepository"""
    repo = AsyncMock(spec=RDBRepository)
    return repo


@pytest.fixture
def mock_chunk_adapter():
    """Мок ChunkAdapterInterface"""
    adapter = MagicMock(spec=ChunkAdapterInterface)
    adapter.split.return_value = ["Chunk 1", "Chunk 2", "Chunk 3"]
    return adapter


@pytest.fixture
def sample_load_data_request(sample_core_document):
    """Запрос на загрузку данных"""
    return LoadDataRequest(
        data=sample_core_document,
        chunk_size=512,
        chunk_overlap=50,
    )


@pytest.fixture
def sample_llm_request(sample_collection_id):
    """Запрос к LLM"""
    return LLMRequest(
        query="Что такое машинное обучение?",
        collection_id=sample_collection_id,
        model="GigaChat",
    )


@pytest.fixture
def sample_search_request(sample_collection_id):
    """Запрос на поиск"""
    return SearchRequest(
        query="машинное обучение",
        collection_id=sample_collection_id,
        model="GigaChat",
        top_k=5,
    )


@pytest.fixture
def sample_create_collection_request():
    """Запрос на создание коллекции"""
    return CreateCollectionRequest(
        name="New Collection",
        description="New Description",
        is_public=False,
    )


@pytest.fixture
def sample_update_collection_request(sample_collection_id):
    """Запрос на обновление коллекции"""
    return UpdateCollectionRequest(
        collection_id=sample_collection_id,
        name="Updated Collection",
        description="Updated Description",
    )


@pytest.fixture
def sample_update_document_request(sample_document_id):
    """Запрос на обновление документа"""
    return UpdateDocumentRequest(
        document_id=sample_document_id,
        title="Updated Title",
        description="Updated Description",
    )

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
