#для непосредственных обращений к серверу через aiohttp
import aiohttp
import json
from aiogram import F, Router
from aiogram.types import  CallbackQuery, BufferedInputFile
from typing import Dict, List
from uuid import UUID

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
        await callback.message.answer("Ошибка подключения")
        await callback.answer()
    #except Exception as e:
        await callback.message.answer("Неизвестная ошибка")
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
                data: Dict[str, int | str] = await response.json()
                if response.status == 201:
                    return f"Коллекция добавлена.\n Название: {data['name']}\n Описание: {data['description']}"
                else:
                    return f"Ошибка: {data['detail']}"
    except aiohttp.ClientError as e:
        return "Ошибка подключения"
    #except Exception as e:
        return "Неизвестная ошибка"

#обновить информацию о коллекции
async def update_coll(user_id: int, coll_id: UUID, name: str, is_public: bool, desc: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                SERVER + API_V + f"/collections/one",
                json={
                        "telegram_id": user_id,
                        "title": name,
                        "description": desc,
                        "is_public": is_public,
                        "collection_id": coll_id
                },
                timeout=aiohttp.ClientTimeout(total=30)) as response:
                return await response.json()
    except aiohttp.ClientError as e:
        return {"detail": f"Ошибка подключения"}
    #except Exception as e:
        return {"detail": "Неизвестная ошибка"}

#добавить документ в коллекцию
async def add_doc(coll_id: UUID, data: Dict, file_bytes: bytes, filename: str):
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
async def get_doc(user_id: int, coll_id: UUID, doc_id: UUID):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                SERVER + API_V + f"/collections/{coll_id}/documents/{doc_id}/?telegram_id={user_id}&document_id={doc_id}",
                timeout=aiohttp.ClientTimeout(total=10)) as response:
                return await response.json()
    except aiohttp.ClientError as e:
        return {"detail": "Ошибка подключения"}
    #except Exception as e:
        return {"detail": "Неизвестная ошибка"}
    
#изменить информацию о документе
async def update_doc(user_id: int,
                     coll_id: UUID,
                     doc_id: UUID,
                     name: str,
                     desc: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                SERVER + API_V + f"/collections/{coll_id}/documents/{doc_id}",
                json={
                        "telegram_id": user_id,
                        "title": name,
                        "description": desc,
                        "document_id": doc_id
                },
                timeout=aiohttp.ClientTimeout(total=30)) as response:
                return await response.json()
    except aiohttp.ClientError as e:
        return {"detail": "Ошибка подключения"}
    #except Exception as e:
        return {"detail": "Неизвестная ошибка"}

#удалить коллекцию
async def delete_collection_server(collection_id: UUID, user_id: int) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                SERVER + API_V + f"/collections/{collection_id}/?telegram_id={user_id}&collection_id={collection_id}",
                timeout=aiohttp.ClientTimeout(total=10)) as response:
                status_text: str = "success"
                if response.status != 204:
                    detail: Dict[str, str] = await response.json()
                    status_text = detail["detail"]
        return status_text
    except aiohttp.ClientError as e:
        return "Ошибка подключения"
    #except Exception as e:
        return "Неизвестная ошибка"
    
#удалить документ из коллекции
async def delete_doc(coll_id: UUID, doc_id: UUID, user_id: int) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                SERVER + API_V + f"/collections/{coll_id}/documents/{doc_id}/?telegram_id={user_id}&document_id={doc_id}",
                timeout=aiohttp.ClientTimeout(total=10)) as response:
                status_text: str = "success"
                if response.status != 204:
                    detail: Dict[str, str] = await response.json()
                    status_text = detail["detail"]
        return status_text
    except aiohttp.ClientError as e:
        return "Ошибка подключения"
    #except Exception as e:
        return "Неизвестная ошибка"
    
#список коллекций для создания клавиатуры
async def view_dbs_internal(user_id: int) -> List[Dict[str, str]]:
    try:
        async with aiohttp.ClientSession() as session:
            print(SERVER + API_V + f"/collections/?telegram_id={user_id}")
            print(type(SERVER + API_V + f"/collections/?telegram_id={user_id}"))
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
        data = [{"error": "Ошибка подключения"}]
        return data
    #except Exception as e:
        data = [{"error": "Неизвестная ошибка"}]
        return data

#список документов для создания клавиатуры
async def view_docs(user_id: int, coll_id: UUID):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                SERVER + API_V + f"collections/{coll_id}/documents/?telegram_id={user_id}&collection_id={coll_id}",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:    
                data: List[Dict[str, str]] = []
                if response.status == 200:
                    data = await response.json()
                else:
                    data = [{"error": "Ошибка сервера"}]
        return data
    except aiohttp.ClientError as e:
        data = [{"error": "Ошибка подключения"}]
        return data
    #except Exception as e:
        data = [{"error": "Неизвестная ошибка"}]
        return data

#отправка rag-запроса
async def send_rag(collection_id: UUID, telegram_id: int, query_text: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                SERVER + API_V + f"/collections/{collection_id}/query",
                json= {
                    "telegram_id": telegram_id,
                    "query_text": query_text,
                    "collection_id": collection_id
                },
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:  
                data = await response.json()
                return data
    except aiohttp.ClientError:
        return {"detail": "Ошибка подключения"}
    #except Exception:
        return {"detail": "Неизвестная ошибка"}
    
#запрос на поиск документов
async def search_docs(collection_id: UUID, telegram_id: int, number_of_sources: int, query_text: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                SERVER + API_V + f"/collections/{collection_id}/find",
                json= {
                    "telegram_id": telegram_id,
                    "number_of_sources": number_of_sources,
                    "query_text": query_text,
                    "collection_id": collection_id
                },
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:  
                data = await response.json()
                return data
    except aiohttp.ClientError as e:
        return {"detail": "Ошибка подключения"}
    #except Exception as e:
        return {"detail": "Неизвестная ошибка"}

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
        return {"detail": "Ошибка подключения"}
    #except Exception as e:
        return {"detail": "Неизвестная ошибка"}

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
        return {"detail": "Ошибка подключения"}
    #except Exception as e:
        return {"detail": "Неизвестная ошибка"}
    
async def is_alive():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                SERVER + API_V + "/health",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:  
                return response
    except aiohttp.ClientError as e:
        return {"detail": "Ошибка подключения"}
    #except Exception as e:
        return {"detail": "Неизвестная ошибка"}