from typing import List
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, status
from src.api.v2.exceptions import handle_exception

from src.api.v2.schemas import Document, Message, SearchRequest
from src.core.application.searching.schemas.search import SearchRequest as SearchRequestForUseCase
from src.core.application.generation.use_cases.answer import AnswerUC
from src.core.application.searching.use_cases.search import SearchUC
from src.core.application.rdb.use_cases.user import GetUserIdUC, CheckAdminUC, GetAttemptCountUC  # не написан

router = APIRouter(tags=["RAG"])

# переписать позже


@router.post("/collections/{collection_id}/query", response_model=Message)
@inject
async def query_rag(
    collection_id: int,
    query_data: SearchRequest,
    preprocess_query: FromDishka[AnswerUC]
):
    """
    Отправить запрос к RAG-системе.
    """
    try:
        response = await preprocess_query.execute(query_data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Ваши бесплатные попытки кончились"
        ) from None

    return response


@router.post("/collections/{collection_id}/find",
             response_model=List[Document])
@inject
async def search_in_collection(
    collection_id: int,
    search_data: SearchRequest,
    search_documents_uc: FromDishka[SearchUC],
    get_user_id_uc: FromDishka[GetUserIdUC],
    check_admin_uc: FromDishka[CheckAdminUC],
    get_attempt_count_uc: FromDishka[GetAttemptCountUC]
):
    """
    Поиск в коллекции.
    """
    try:
        user_id: UUID = await get_user_id_uc.execute(search_data.telegram_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Регистрация пользователей не реализована"
        ) from None

    try:
        attempts_count: int = await get_attempt_count_uc.execute(user_id)
        is_admin: bool = await check_admin_uc.execute(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        ) from None

    if attempts_count >= 10 and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Ваши бесплатные попытки кончились"
        ) from None

    try:
        results = await search_documents_uc.execute(SearchRequestForUseCase(
            query=search_data.query_text,
            model="GigaChat",
            collection_name=collection_id,
            top_k=search_data.number
        ))
    except Exception as exc:
        return handle_exception(exc)

    return [Document(
        document_id=doc.metadata.get("document_id", ""),
        title=doc.metadata.get("title", ""),
        description=doc.metadata.get("description", ""),
        file_name=doc.metadata.get("file_name", ""),
        file_size=doc.metadata.get("file_size", 0),
        created_at=doc.metadata.get("created_at", None),
        metadata={
            "url": doc.metadata.get("url", None),
            "relevance": doc.metadata.get("relevance", 0)
        }
    ) for doc in results]
