from http import HTTPStatus
from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject

from src.api.v1.schemas import RagRequest, RagResponse
from src.core.application.generation.use_cases.answer import AnswerUS


search_router = APIRouter(
    prefix="/rag",
    tags=["Использование RAG-системы"]
)


@search_router.post("/query", status_code=HTTPStatus.OK)
@inject
async def answer_query(
        request: RagRequest,
        answer_uc: FromDishka[AnswerUS]) -> RagResponse:
    """
    TODO: реализовать запись в статистику, вызов
          AnswerUC, возврат в нужном типе и пр.
    """
    ...
