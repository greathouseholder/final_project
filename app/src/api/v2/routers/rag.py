from typing import List

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, status

from src.api.v2.schemas import DocumentRelevance, Message, SearchRequest
from src.core.application.embeddings import SearchUC
from src.core.application.generation.use_cases.answer import AnswerUC

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

# переписать позже


@router.post("/collections/{collection_id}/find",
             response_model=List[DocumentRelevance])
@inject
async def search_in_collection(
    collection_id: int,
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
        ) from None

    return results
