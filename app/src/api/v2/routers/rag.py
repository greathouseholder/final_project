from typing import List
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, status

from src.api.v2.exceptions import handle_exception
from src.api.v2.helpers import check_admin_rights, get_user_id
from src.api.v2.schemas import Document, SearchRequest
from src.core.application.generation.schemas.answer import LLMRequest
from src.core.application.generation.use_cases.answer import AnswerUC
from src.core.application.rdb.use_cases.user import (
    CheckAdminUC,
    CheckPaymentUC,
    GetAttemptCountUC,
    RegisterUserUC,
)
from src.core.application.searching.schemas.search import SearchRequest as SearchRequestForUseCase
from src.core.application.searching.use_cases.search import SearchUC

router = APIRouter(tags=["RAG"])


@router.post("/collections/{collection_id}/query")
@inject
async def query_rag(
    query_data: SearchRequest,
    generate_answer_uc: FromDishka[AnswerUC],
    register_user_uc: FromDishka[RegisterUserUC],
    check_admin_uc: FromDishka[CheckAdminUC],
    get_attempt_count_uc: FromDishka[GetAttemptCountUC],
    check_payment_uc: FromDishka[CheckPaymentUC]
):
    """
    Отправить запрос к RAG-системе.
    """
    try:
        user_id = await get_user_id(query_data.telegram_id, None, register_user_uc)
        attempts_count: int = await get_attempt_count_uc.execute(user_id)
        is_admin: bool = await check_admin_rights(user_id, check_admin_uc)
        is_paid: bool = await check_payment_uc.execute(user_id)

        if attempts_count >= 10 and not is_admin and not is_paid:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Ваши бесплатные попытки кончились"
            ) from None

        llm_response, core_documents = await generate_answer_uc.execute(
            LLMRequest(
                query=query_data.query_text,
                model="Gigachat",
                collection_id=query_data.collection_id
            )
        )

        return {
            "content": llm_response.response_text,
            "sources": core_documents
        }
    except Exception as exc:
        raise handle_exception(exc) from None


@router.post("/collections/{collection_id}/find",
             response_model=List[Document])
@inject
async def search_in_collection(
    search_data: SearchRequest,
    search_documents_uc: FromDishka[SearchUC],
    register_user_uc: FromDishka[RegisterUserUC],
    check_admin_uc: FromDishka[CheckAdminUC],
    get_attempt_count_uc: FromDishka[GetAttemptCountUC],
    check_payment_uc: FromDishka[CheckPaymentUC]
):
    """
    Поиск в коллекции.
    """
    try:
        user_id = await get_user_id(search_data.telegram_id, None, register_user_uc)
        attempts_count: int = await get_attempt_count_uc.execute(user_id)
        is_admin: bool = await check_admin_rights(user_id, check_admin_uc)
        is_paid: bool = await check_payment_uc.execute(user_id)

        if attempts_count >= 10 and not is_admin and not is_paid:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Ваши бесплатные попытки кончились"
            ) from None

        results = await search_documents_uc.execute(SearchRequestForUseCase(
            query=search_data.query_text,
            model="GigaChat",
            collection_id=search_data.collection_id,
            top_k=search_data.number
        ))

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
    except Exception as exc:
        raise handle_exception(exc) from None
