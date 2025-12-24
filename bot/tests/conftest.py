import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID
from aiogram import Bot
from aiogram.types import User, Chat, Message, CallbackQuery, Document, SuccessfulPayment, PreCheckoutQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage

@pytest.fixture
def bot() -> MagicMock:
    """Мок бота"""
    mock_bot = AsyncMock(spec=Bot)
    mock_bot.id = 123456789
    return mock_bot

@pytest.fixture
def storage() -> MemoryStorage:
    """Реальное хранилище состояний для тестов"""
    return MemoryStorage()

@pytest.fixture
def user() -> User:
    """Тестовый пользователь"""
    return User(
        id=12345678,
        is_bot=False,
        first_name="Test",
        last_name="User",
        username="testuser",
        language_code="ru"
    )

@pytest.fixture
def chat() -> Chat:
    """Тестовый чат"""
    return Chat(
        id=12345678,
        type="private",
        first_name="Test",
        last_name="User",
        username="testuser"
    )

@pytest.fixture
def state(bot, storage, user, chat) -> FSMContext:
    """FSMContext для тестов"""
    key = StorageKey(
        bot_id=bot.id,
        chat_id=chat.id,
        user_id=user.id
    )
    return FSMContext(storage=storage, key=key)

@pytest.fixture
async def fsm_context(storage):
    return FSMContext(storage=storage, key="test_key")

@pytest.fixture
def message(user, chat, bot) -> MagicMock:
    """Мок сообщения с нужными методами"""
    msg = MagicMock(spec=Message)
    msg.from_user = user
    msg.chat = chat
    msg.text = "Test message"
    msg.message_id = 1
    msg.document = Document(
        file_id="test_file_id",
        file_name="test.txt",
        file_unique_id="test_unique_id"
    )
    # Async методы
    msg.answer = AsyncMock(return_value=MagicMock(message_id=2))
    msg.answer_photo = AsyncMock()
    msg.answer_audio = AsyncMock()
    msg.answer_document = AsyncMock()
    msg.edit_text = AsyncMock()
    msg.delete = AsyncMock()
    return msg

@pytest.fixture
def callback_query(user, chat, message, bot) -> MagicMock:
    """Мок callback query"""
    callback = MagicMock(spec=CallbackQuery)
    callback.id = "test_callback_id"
    callback.from_user = user
    callback.message = message
    callback.chat = chat
    callback.data = ""
    callback.answer = AsyncMock()
    return callback

@pytest.fixture
def sample_collections():
    """Тестовые коллекции"""
    return [
        {"collection_id": "1", "name": "Коллекция 1"},
        {"collection_id": "2", "name": "Коллекция 2"},
        {"collection_id": "3", "name": "Коллекция 3"},
    ]

@pytest.fixture
def sample_documents():
    """Тестовые документы"""
    return [
        {"document_id": "1", "name": "Документ 1"},
        {"document_id": "2", "name": "Документ 2"},
    ]

@pytest.fixture
def sample_rag_response():
    """Тестовый ответ RAG"""
    return {
        "content": "Это ответ на ваш вопрос.",
        "sources": [
            {"title": "Источник 1", "url": "https://example.com/1"},
            {"title": "Источник 2", "url": "https://example.com/2"},
        ]
    }

@pytest.fixture
def sample_search_response():
    """Тестовый ответ поиска документов"""
    return {
        "title": "Найденный документ",
        "file_name": "document.pdf",
        "file_size": "2.5",
        "created_at": "2024-01-15",
        "metadata": {"url": "https://example.com/doc"}
    }

@pytest.fixture
def valid_uuid():
    return UUID("123e4567-e89b-12d3-a456-426614174000")

@pytest.fixture
def pre_checkout_query(user):
    pcq = AsyncMock(spec=PreCheckoutQuery)
    pcq.from_user = user
    pcq.id = "pre_checkout_123"
    return pcq

@pytest.fixture
def successful_payment_message(user, chat):
    msg = AsyncMock(spec=Message)
    msg.from_user = user
    msg.chat = chat
    msg.successful_payment = SuccessfulPayment(
        total_amount=10000,
        currency="RUB",
        invoice_payload="sub1"
    )
    return msg