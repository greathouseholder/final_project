from src.api.v1.schemas import SearchRequest as SearchRequestAPI
from src.core.application.searching.schemas.search import SearchRequest as SearchRequestUC


def get_search_uc_request(request: SearchRequestAPI) -> SearchRequestUC:
    return SearchRequestUC(
        query=request.query_text,
        # потенцильно можно реализовать выбор модели
        model="",
        collection_name=request.database_id
    )
