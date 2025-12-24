from dishka import make_async_container

from .business_logic.answer_provider import AnswerUCProvider
from .business_logic.load_data_provider import LoadingUCProvider
from .business_logic.search_provider import SearchUCProvider
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
    SearchUCProvider(),
    AnswerUCProvider(),
    LoadingUCProvider(),
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
