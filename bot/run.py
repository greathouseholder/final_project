import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN
from bot_app.handlers.commands_handlers import router_commands
from bot_app.handlers.keyboard_handlers import keyboard_router
from bot_app.handlers.server_handlers import server_router
from bot_app.handlers.rag_handlers import rag_router
from bot_app.handlers.doc_search_handlers import doc_search_router
from bot_app.handlers.collections_handlers import collections_router
from bot_app.handlers.documents_handlers import documents_router

bot: Bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp: Dispatcher = Dispatcher()

async def main() -> None:
    dp.include_routers(router_commands,
                       keyboard_router,
                       server_router,
                       rag_router,
                       doc_search_router,
                       collections_router,
                       documents_router)
    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
