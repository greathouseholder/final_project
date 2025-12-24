import pytest

from aiogram.types import Message, User, Chat
from unittest.mock import MagicMock
import bot_app.handlers.commands_handlers as ch

@pytest.mark.asyncio
async def test_cmd_start_sends_hello_message(message):

    message.text = "/start"
    message.entities = [{"type": "bot_command", "offset": 0, "length": 6}]

    await ch.cmd_start(message)

    assert message.answer.call_count == 1

    assert message.answer.call_args[0][0] == "Приветствуем тебя, ковбой! " \
    "Для просмотра доступных команд введи /help ." \
    "Выбери панель:"
    assert message.answer.call_args[1]["reply_markup"] == ch.kb.main_menu
    assert message.answer.called