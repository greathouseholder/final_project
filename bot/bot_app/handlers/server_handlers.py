#для непосредственных обращений к серверу через aiohttp
import aiohttp
import json
from aiogram import F, Router
from aiogram.types import  CallbackQuery, BufferedInputFile
from typing import Dict, List

from config import SERVER, API_V


server_router: Router = Router()

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
                                description: str,
                                is_public: bool) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                SERVER + API_V + "/collections",
                json={"telegram_id": telegram_id,
                      "name": name.strip(),
                      "description": description.strip(),
                      "is_public": is_public
                      },
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 201:
                    data: Dict[str, int | str] = response.json()
                    return f"Коллекция добавлена.\n Название: {data['name']}\n Описание: {data['description']}"
                else:
                    return f"Ошибка: {response.content['detail']}"
    except aiohttp.ClientError as e:
        return f"Ошибка подключения: {str(e)}"
    except Exception as e:
        return f"Неизвестная ошибка: {str(e)}"

#обновить информацию о коллекции
async def update_coll(user_id: int, coll_id: int, name: str, desc: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                SERVER + API_V + f"/collections/{coll_id}",
                json={
                        "telegram_id": user_id,
                        "title": name,
                        "description": desc
                },
                timeout=aiohttp.ClientTimeout(total=30)) as response:
                return await response.json()
    except aiohttp.ClientError as e:
        return {"detail": f"Ошибка подключения: {str(e)}"}
    except Exception as e:
        return {"detail": f"Неизвестная ошибка: {str(e)}"}

#добавить документ в коллекцию
async def add_doc(coll_id: int, data: Dict, file_bytes: bytes, filename: str):
     async with aiohttp.ClientSession() as session:
        form_data = aiohttp.FormData()
        form_data.add_field(
            'metadata',
            json.dumps(data, ensure_ascii=False),
            content_type='application/json'
        )

        form_data.add_field(
            'file',
            file_bytes,
            filename=filename,
            content_type='text/plain'
        )
        
        async with session.post(
            SERVER + API_V + f"/collections/{coll_id}/documents",
            data=form_data,
            timeout=aiohttp.ClientTimeout(total=30)
        ) as response:
            return await response.json()

#посмотреть информацию о документе
async def get_doc(user_id: int, coll_id: int, doc_id: int):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                SERVER + API_V + f"/collections/{coll_id}/documents/{doc_id}/?telegram_id={user_id}",
                timeout=aiohttp.ClientTimeout(total=10)) as response:
                return await response.json()
    except aiohttp.ClientError as e:
        return {"detail": f"Ошибка подключения: {str(e)}"}
    except Exception as e:
        return {"detail": f"Неизвестная ошибка: {str(e)}"}
    
#изменить информацию о документе
async def update_doc(user_id: int,
                     coll_id: int,
                     doc_id: int,
                     name: str,
                     desc: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                SERVER + API_V + f"/collections/{coll_id}/documents/{doc_id}",
                json={
                        "telegram_id": user_id,
                        "title": name,
                        "description": desc
                },
                timeout=aiohttp.ClientTimeout(total=30)) as response:
                return await response.json()
    except aiohttp.ClientError as e:
        return {"detail": f"Ошибка подключения: {str(e)}"}
    except Exception as e:
        return {"detail": f"Неизвестная ошибка: {str(e)}"}

#удалить коллекцию
async def delete_collection_server(collection_id: str, user_id: int) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                SERVER + API_V + f"/collections/{collection_id}/?telegram_id={user_id}",
                timeout=aiohttp.ClientTimeout(total=10)) as response:
                status_text: str = "success"
                if response.status != 204:
                    detail: Dict[str, str] = await response.json()
                    status_text = detail["detail"]
        return status_text
    except aiohttp.ClientError as e:
        return f"Ошибка подключения: {str(e)}"
    except Exception as e:
        return f"Неизвестная ошибка: {str(e)}"
    
#удалить документ из коллекции
async def delete_doc(coll_id: int, doc_id: int, user_id: int) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                SERVER + API_V + f"/collections/{coll_id}/documents/{doc_id}/?telegram_id={user_id}",
                timeout=aiohttp.ClientTimeout(total=10)) as response:
                status_text: str = "success"
                if response.status != 204:
                    detail: Dict[str, str] = await response.json()
                    status_text = detail["detail"]
        return status_text
    except aiohttp.ClientError as e:
        return f"Ошибка подключения: {str(e)}"
    except Exception as e:
        return f"Неизвестная ошибка: {str(e)}"
    
#список коллекций для создания клавиатуры
async def view_dbs_internal(user_id: int) -> List[Dict[str, str]]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                SERVER + API_V + f"/collections/?telegram_id={user_id}",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:    
                data: List[Dict[str, str]] = []
                if response.status == 200:
                    data = await response.json()
                else:
                    data = [{"error": "Ошибка сервера"}]
        return data
    except aiohttp.ClientError as e:
        data = [{"error": f"Ошибка подключения: {str(e)}"}]
        return data
    except Exception as e:
        data = [{"error": f"Неизвестная ошибка: {str(e)}"}]
        return data

#список документов для создания клавиатуры
async def view_docs(user_id: int, coll_id: int):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                SERVER + API_V + f"collections/{coll_id}/documents/?telegram_id={user_id}",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:    
                data: List[Dict[str, str]] = []
                if response.status == 200:
                    data = await response.json()
                else:
                    data = [{"error": "Ошибка сервера"}]
        return data
    except aiohttp.ClientError as e:
        data = [{"error": f"Ошибка подключения: {str(e)}"}]
        return data
    except Exception as e:
        data = [{"error": f"Неизвестная ошибка: {str(e)}"}]
        return data

#отправка rag-запроса
async def send_rag(collection_id: int, telegram_id: int, query_text: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                SERVER + API_V + f"/collections/{collection_id}/query",
                json= {
                    "telegram_id": telegram_id,
                    "query_text": query_text
                },
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:  
                data = await response.json()
                if "detail" in data:
                    return '', data
                return data["content"], data["sources"]
    except aiohttp.ClientError as e:
        return '', {"detail": f"Ошибка подключения: {str(e)}"}
    except Exception as e:
        return '', {"detail": f"Неизвестная ошибка: {str(e)}"}
    
#запрос на поиск документов
async def search_docs(collection_id: int, telegram_id: int, number_of_sources: int, query_text: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                SERVER + API_V + f"/collections/{collection_id}/find",
                json= {
                    "telegram_id": telegram_id,
                    "number_of_sources": number_of_sources,
                    "query_text": query_text
                },
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:  
                data = await response.json()
                return data
    except aiohttp.ClientError as e:
        return {"detail": f"Ошибка подключения: {str(e)}"}
    except Exception as e:
        return {"detail": f"Неизвестная ошибка: {str(e)}"}

#куплена ли подписка
async def is_paid(user_id: int):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                SERVER + API_V + f"/users/payment/?telegram_id={user_id}",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:  
                data = await response.json()
                return data
    except aiohttp.ClientError as e:
        return {"detail": f"Ошибка подключения: {str(e)}"}
    except Exception as e:
        return {"detail": f"Неизвестная ошибка: {str(e)}"}

#оплата прошла успешно
async def subscription(user_id: int):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                SERVER + API_V + f"/users/payment",
                json= {
                    "telegram_id": user_id,
                },
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:  
                pass
    except aiohttp.ClientError as e:
        return {"detail": f"Ошибка подключения: {str(e)}"}
    except Exception as e:
        return {"detail": f"Неизвестная ошибка: {str(e)}"}