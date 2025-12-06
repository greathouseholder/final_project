from dishka import make_async_container
from .search_provider import SearchProvider
from .answer_provider import AnswerProvider
from .load_data_provider import LoadDataProvider


container = make_async_container(
    SearchProvider(),
    AnswerProvider(),
    LoadDataProvider())


__all__ = ("container",)
