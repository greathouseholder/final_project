#для непосредственных обращений к серверу через aiohttp
import aiohttp
import json
from aiogram import F, Router
from aiogram.types import  CallbackQuery, BufferedInputFile
from typing import Dict, List

from config import SERVER


server_router: Router = Router()

@server_router.callback_query(F.data == 'view_dbs_names')
async def view_dbs_names(callback: CallbackQuery) -> None:
    await callback.answer('Запрашиваю базы данных...')
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                SERVER + "/api/v1/search/databases",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:    
                if response.status == 200:
                    data: Dict[str, List[Dict[str, str]]] = await response.json()
                    status_text: str = ''
                    for database in data.get("databases"):
                        status_text += f'{database.get("name")}\n' 
                else:
                    status_text: str = f"Ошибка сервера: {response.status}"
                await callback.message.answer(
                        text=status_text,
                        parse_mode="Markdown"
                    ) if status_text else await callback.message.answer(
                        text="Баз данных не найдено",
                        parse_mode="Markdown"
                    )
    except aiohttp.ClientError as e:
        await callback.message.answer(f"Ошибка подключения: {str(e)}")
        await callback.answer()
    except Exception as e:
        await callback.message.answer(f"Неизвестная ошибка: {str(e)}")
        await callback.answer()

@server_router.callback_query(F.data == 'view_dbs')
async def view_dbs(callback: CallbackQuery) -> None:
    await callback.answer('Запрашиваю базы данных...')
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                SERVER + "/api/v1/search/databases",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:    
                if response.status == 200:
                    data: Dict[str, List[Dict[str, str]]] = await response.json()
                    status_text = 'Базы данных не найдены' if not data else ''
                    if data:
                        json_text = json.dumps(data)
                        await callback.message.answer_document(
                            document=BufferedInputFile(
                                json_text.encode('utf-8'),
                                filename="databases.txt"
                            )
                        )
                else:
                    status_text: str = f"Ошибка сервера: {response.status}"
                if status_text:
                    await callback.message.answer(
                            text=status_text,
                            parse_mode="Markdown"
                        )
    except aiohttp.ClientError as e:
        await callback.message.answer(f"Ошибка подключения: {str(e)}")
        await callback.answer()
    except Exception as e:
        await callback.message.answer(f"Неизвестная ошибка: {str(e)}")
        await callback.answer()