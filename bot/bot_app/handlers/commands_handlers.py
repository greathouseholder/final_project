#для обработок команд (начинающихся с /)
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile

from bot_app import keyboards as kb


router_commands: Router = Router()

@router_commands.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer("Приветствуем тебя, ковбой! " \
    "Для просмотра доступных команд введи /help ." \
    "Выбери панель:", reply_markup=kb.panels)

@router_commands.message(Command('call_saul'))
async def cmd_call_saul(message: Message) -> None:
    await message.answer_audio(
            audio=FSInputFile("audio/track.m4a"),
            caption="Кто прочитал тот лох",
            performer="Unknown",
            title="Better Call Saul"
        )

@router_commands.message(Command('help'))
async def cmd_help(message: Message) -> None:
    await message.answer("Доступные команды: \n"
    "/call_saul\n"
    "/get_my_photo", reply_markup=kb.return_button_keyboard)

@router_commands.message(Command('get_my_photo'))
async def get_photo(message: Message) -> None:
    await message.answer_photo(photo='https://alisa-yar.ru/images/articles/article-1.jpg',
                               caption="Это ты")
    