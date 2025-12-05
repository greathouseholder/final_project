from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Доступные команды: \n"
    "/call_saul\n"
    "/get_my_photo")

@router.message(Command('call_saul'))
async def cmd_call_saul(message: Message):
    await message.answer_audio(
            audio=FSInputFile("audio/track.m4a"),
            caption="Кто прочитал тот лох",
            performer="Unknown",
            title="Better Call Saul"
        )
    
@router.message(Command('get_my_photo'))
async def get_photo(message: Message):
    await message.answer_photo(photo='https://alisa-yar.ru/images/articles/article-1.jpg',
                               caption="Это ты")