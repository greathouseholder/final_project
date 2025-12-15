#для непосредственных обращений к серверу через aiohttp
import aiohttp
import json
from aiogram import F, Router
from aiogram.types import  CallbackQuery, BufferedInputFile
from typing import Dict, List

from config import SERVER, API_V


server_router: Router = Router()

#посмотреть названия коллекций
@server_router.callback_query(F.data == 'view_dbs_names')
async def view_dbs_names(callback: CallbackQuery) -> None:
    await callback.answer('Запрашиваю базы данных...')
    user_id: int = callback.from_user.id
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                SERVER + API_V + f"/collections/?telegram_id={user_id}",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:    
                if response.status == 200:
                    data: Dict[str, List[Dict[str, str]]] = await response.json()
                    status_text: str = ''
                    for collection in data.get("collections"):
                        status_text += f'{collection.get("name")}\n' 
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

#получить полную информацию о коллекциях
@server_router.callback_query(F.data == 'view_dbs')
async def view_dbs(callback: CallbackQuery) -> None:
    await callback.answer('Запрашиваю базы данных...')
    user_id: int = callback.from_user.id
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                SERVER + API_V + f"/collections/?telegram_id={user_id}",
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

#добавить новую коллекцию
async def add_collection_server(telegram_id: int,
                                name: str,
                                description: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                SERVER + "/api/v1/search/databases",
                json={"telegram_id": telegram_id,
                      "name": name.strip(),
                      "description": description.strip()
                      },
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 201:
                    data: Dict[str, int | str] = response.json
                    return f"Коллекция добавлена.\n Название: {data['name']}\n Описание: {data['description']}"
                else:
                    return f"Ошибка: {response.content['detail']}"
    except aiohttp.ClientError as e:
        return f"Ошибка подключения: {str(e)}"
    except Exception as e:
        return f"Неизвестная ошибка: {str(e)}"

#удалить коллекцию
async def delete_collection_server(collection_name: str, user_id: int) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                SERVER + API_V + f"/collections/?telegram_id={user_id}",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    dbs: Dict[str, List[Dict[str, str]]] = await response.json()
                    status_text = 'Базы данных не найдены' if not dbs else 'success'
                else:
                    status_text: str = f"Ошибка сервера: {response.status}"
            if not dbs:
                return status_text
            collection_id: int | None = None
            for collection in dbs["collections"]:
                if collection["name"] == collection_name:
                    collection_id = collection["collection_id"]
                    break
            if collection_id is None:
                return 'Коллекция не найдена'
            async with session.delete(SERVER + API_V + f"/collections/{collection_id}/?telegram_id={user_id}",
                timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status != 204:
                    detail: Dict[str, str] = await response.json()
                    status_text = detail["detail"]
        return status_text
    except aiohttp.ClientError as e:
        return f"Ошибка подключения: {str(e)}"
    except Exception as e:
        return f"Неизвестная ошибка: {str(e)}"
    