from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery

from bot_app import keyboards as kb


router_commands = Router()
router_keyboard = Router()

@router_commands.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Доступные команды: \n"
    "/call_saul\n"
    "/get_my_photo", reply_markup=kb.panels)

@router_commands.message(Command('call_saul'))
async def cmd_call_saul(message: Message):
    await message.answer_audio(
            audio=FSInputFile("audio/track.m4a"),
            caption="Кто прочитал тот лох",
            performer="Unknown",
            title="Better Call Saul"
        )

@router_commands.message(Command('get_my_photo'))
async def get_photo(message: Message):
    await message.answer_photo(photo='https://alisa-yar.ru/images/articles/article-1.jpg',
                               caption="Это ты")
    
@router_keyboard.callback_query(F.data == 'user_panel')
async def user_panel(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите действие', reply_markup=kb.user_actions)

@router_keyboard.callback_query(F.data == 'admin_panel')
async def user_panel(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите действие', reply_markup=kb.admin_actions)

@router_keyboard.callback_query(F.data == 'return')
async def user_panel(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите панель', reply_markup=kb.panels)

@router_keyboard.callback_query(F.data == 'user_query')
async def user_panel(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Введите запрос:')
