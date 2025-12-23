from dishka import make_async_container

from .business_logic.answer_provider import AnswerProvider
from .business_logic.load_data_provider import LoadDataProvider
from .business_logic.search_provider import SearchProvider
from .rdb_scenarios.collections_uc_providers import CollectionUseCasesProvider
from .rdb_scenarios.documents_uc_providers import DocumentUseCasesProvider
from .rdb_scenarios.users_uc_providers import UserUseCasesProvider
from .utils import (
    BGERerankerProvider,
    DatabaseProvider,
    FridaEmbedderProvider,
    GigachatProvider,
    JinjaProvider,
    LangChainProvider,
    LLMPreprocessorProvider,
    QdrantProvider,
    SQLAlchemyRDBRepositoryProvider,
    ValidationProvider,
)

container = make_async_container(
    SearchProvider(),
    AnswerProvider(),
    LoadDataProvider(),
    CollectionUseCasesProvider(),
    DocumentUseCasesProvider(),
    UserUseCasesProvider(),
    BGERerankerProvider(),
    DatabaseProvider(),
    FridaEmbedderProvider(),
    GigachatProvider(),
    JinjaProvider(),
    LangChainProvider(),
    LLMPreprocessorProvider(),
    QdrantProvider(),
    SQLAlchemyRDBRepositoryProvider(),
    ValidationProvider(),
)


__all__ = ("container",)
