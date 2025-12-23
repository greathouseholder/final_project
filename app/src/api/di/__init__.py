from dishka import make_async_container

from .business_logic.answer_provider import AnswerProvider
from .business_logic.load_data_provider import LoadDataProvider
from .business_logic.search_provider import SearchProvider

container = make_async_container(SearchProvider(), AnswerProvider(), LoadDataProvider())


__all__ = ("container",)
