from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from dishka.integrations.fastapi import FromDishka, inject

from src.api.v1.schemas import SearchRequest, SearchResponse
from src.core.application.searching.use_cases.search import SearchUC
from src.infra.adapters.api import get_api_do_entity
from src.infra.adapters.api import get_search_uc_request


search_router = APIRouter(
    prefix="/search",
    tags=["Поиск документа"]
)


@search_router.post("/documents", status_code=HTTPStatus.OK)
@inject
async def search_for_documents(
        request: SearchRequest,
        search_uc: FromDishka[SearchUC]) -> SearchResponse:
    # TODO: реализовать быстрый поиск до DB с обработкой исключения
    search_request = get_search_uc_request(request)
    core_documents = await search_uc.execute(search_request)
    documents = [get_api_do_entity(doc) for doc in core_documents]
    return SearchResponse(
        documents=documents
    )
