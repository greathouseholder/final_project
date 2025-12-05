import aiogram
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await bot.send_audio(
            chat_id=message.chat.id,
            audio=FSInputFile("audio/track.m4a"),
            caption="Кто прочитал тот лох",
            performer="Unknown",
            title="Better Call Saul"
        )
    

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
