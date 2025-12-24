import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException

from src.api.v2.routers.rag import query_rag, search_in_collection
from src.core.application.generation.schemas.answer import LLMResponse
from src.core.domain.document import CoreDocument


# --- Fixtures для роутера ---

@pytest.fixture
def mock_generate_answer_uc():
    uc = AsyncMock()
    uc.execute.return_value = (
        LLMResponse(model="test", response_text="Router Answer"),
        [CoreDocument(text="doc1", metadata={})]
    )
    return uc


@pytest.fixture
def mock_search_uc(sample_extended_documents):
    uc = AsyncMock()
    # Возвращаем список CoreDocument, как ожидается от SearchUC.execute
    docs = [CoreDocument(text=d.text, metadata=d.metadata) for d in sample_extended_documents]
    uc.execute.return_value = docs
    return uc


@pytest.fixture
def mock_register_user_uc():
    return AsyncMock()


@pytest.fixture
def mock_check_admin_uc():
    return AsyncMock()


@pytest.fixture
def mock_get_attempt_count_uc():
    uc = AsyncMock()
    uc.execute.return_value = 5  # 5 попыток (меньше лимита 10)
    return uc


@pytest.fixture
def mock_check_payment_uc():
    uc = AsyncMock()
    uc.execute.return_value = False  # Не платил
    return uc


# --- Tests ---

@pytest.mark.asyncio
async def test_query_rag_success(
        sample_search_request,
        mock_generate_answer_uc,
        mock_register_user_uc,
        mock_check_admin_uc,
        mock_get_attempt_count_uc,
        mock_check_payment_uc,
        sample_user_id
):
    # Патчим хелперы, которые используются внутри роутера
    with patch("src.api.v2.routers.rag.get_user_id", new=AsyncMock(return_value=sample_user_id)), \
            patch("src.api.v2.routers.rag.check_admin_rights", new=AsyncMock(return_value=False)):
        result = await query_rag(
            query_data=sample_search_request,
            generate_answer_uc=mock_generate_answer_uc,
            register_user_uc=mock_register_user_uc,
            check_admin_uc=mock_check_admin_uc,
            get_attempt_count_uc=mock_get_attempt_count_uc,
            check_payment_uc=mock_check_payment_uc
        )

        assert result["content"] == "Router Answer"
        assert len(result["sources"]) == 1
        mock_generate_answer_uc.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_query_rag_limit_exceeded(
        sample_search_request,
        mock_generate_answer_uc,
        mock_register_user_uc,
        mock_check_admin_uc,
        mock_get_attempt_count_uc,
        mock_check_payment_uc,
        sample_user_id
):
    # Симулируем: 10 попыток, не админ, не платил
    mock_get_attempt_count_uc.execute.return_value = 10

    with patch("src.api.v2.routers.rag.get_user_id", new=AsyncMock(return_value=sample_user_id)), \
            patch("src.api.v2.routers.rag.check_admin_rights", new=AsyncMock(return_value=False)):
        # Ожидаем 429 ошибку
        with pytest.raises(HTTPException) as exc:
            await query_rag(
                query_data=sample_search_request,
                generate_answer_uc=mock_generate_answer_uc,
                register_user_uc=mock_register_user_uc,
                check_admin_uc=mock_check_admin_uc,
                get_attempt_count_uc=mock_get_attempt_count_uc,
                check_payment_uc=mock_check_payment_uc
            )

        assert exc.value.status_code == 429
        mock_generate_answer_uc.execute.assert_not_called()


@pytest.mark.asyncio
async def test_search_in_collection_success(
        sample_search_request,
        mock_search_uc,
        mock_register_user_uc,
        mock_check_admin_uc,
        mock_get_attempt_count_uc,
        mock_check_payment_uc,
        sample_user_id
):
    with patch("src.api.v2.routers.rag.get_user_id", new=AsyncMock(return_value=sample_user_id)), \
            patch("src.api.v2.routers.rag.check_admin_rights", new=AsyncMock(return_value=False)):
        result = await search_in_collection(
            search_data=sample_search_request,
            search_documents_uc=mock_search_uc,
            register_user_uc=mock_register_user_uc,
            check_admin_uc=mock_check_admin_uc,
            get_attempt_count_uc=mock_get_attempt_count_uc,
            check_payment_uc=mock_check_payment_uc
        )

        assert isinstance(result, list)
        assert len(result) > 0
        assert result[0].title == "Title 0"  # Из sample_extended_documents фикстуры
        mock_search_uc.execute.assert_awaited_once()