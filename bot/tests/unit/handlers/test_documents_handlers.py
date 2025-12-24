import pytest
from unittest.mock import AsyncMock, MagicMock

import bot_app.handlers.documents_handlers as dh

@pytest.mark.asyncio
async def test_view_docs_empty_list(callback_query, fsm_context, valid_uuid, monkeypatch):
    
    async def mock_view_docs(user_id, coll_id):
        return []
    monkeypatch.setattr("bot_app.handlers.server_handlers.view_docs", mock_view_docs)

    await fsm_context.update_data(id=valid_uuid)

    await dh.view_docs(callback_query, state=fsm_context)

    assert callback_query.answer.call_count == 1
    assert callback_query.message.answer.call_count == 1
    assert "Список документов пуст" in callback_query.message.answer.call_args[0][0]

    current_state = await fsm_context.get_state()
    assert current_state is None
    data = await fsm_context.get_data()

@pytest.mark.asyncio
async def test_view_docs_success(callback_query, fsm_context, valid_uuid, monkeypatch):

    test_docs = [
        {"id": "doc1", "title": "Документ 1"},
        {"id": "doc2", "title": "Документ 2"}
    ]

    async def mock_view_docs(user_id, coll_id):
        return test_docs
    monkeypatch.setattr("bot_app.handlers.server_handlers.view_docs", mock_view_docs)

    await fsm_context.update_data(id=valid_uuid)
    await dh.view_docs(callback_query, state=fsm_context)

    data = await fsm_context.get_data()
    assert data["documents"] == test_docs
    assert data["docs"] == test_docs
    assert data["current_page"] == 0

    assert callback_query.message.edit_text.call_count == 1
    call_args, call_kwargs = callback_query.message.edit_text.call_args
    assert 'Вот все документы из коллекции' in call_args[0]
    assert "reply_markup" in call_kwargs

    assert call_kwargs["reply_markup"] is not None

@pytest.mark.asyncio
async def test_add_doc_success(message, fsm_context, valid_uuid, monkeypatch):

    message.bot.get_file = AsyncMock(return_value=MagicMock(file_path="path/to/file"))
    message.bot.download_file = AsyncMock(return_value=b"file content")

    await fsm_context.update_data(
        id=str(valid_uuid),
        name="Тест документ",
        desc="Описание теста",
        url="https://test.com"
    )

    monkeypatch.setattr(
        "bot_app.handlers.server_handlers.add_doc",
        AsyncMock(return_value={"id": "doc123"})
    )

    await dh.add_doc(message, state=fsm_context)

    assert message.bot.get_file.call_count == 1
    assert message.bot.download_file.call_count == 1

    assert message.answer.call_count == 1
    call_args = message.answer.call_args[0][0]
    assert "Документ добавлен" in call_args
    assert "Тест документ" in call_args
    assert "Описание теста" in call_args
    assert "https://test.com" in call_args

    current_state = await fsm_context.get_state()
    assert current_state is None
