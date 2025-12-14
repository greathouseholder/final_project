from typing import List

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, status

from src.api.v2.schemas import DocumentRelevance, Message, SearchRequest
from src.core.application.databases import CheckAdminUC
from src.core.application.embeddings import PreProcessQueryUC, SearchUC

router = APIRouter(tags=["RAG"])

@router.post("/conversations/{conversation_id}/query", response_model=Message)
@inject
async def query_rag(
    conversation_id: int,
    query_data: SearchRequest,
    preprocess_query: FromDishka[PreProcessQueryUC]
):
    """
    Отправить запрос к RAG-системе.
    """
    try:
        response = await preprocess_query.execute(query_data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Диалог не найден"
        )

    return response

@router.post("/collections/find", response_model=List[DocumentRelevance])
@inject
async def search_in_collection(
    search_data: SearchRequest,
    search_documents: FromDishka[SearchUC]
):
    """
    Поиск в коллекции.
    """
    try:
        results = await search_documents.execute(search_data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Ваши бесплатные попытки кончились"
        )

    return results
