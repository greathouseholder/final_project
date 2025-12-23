from app.src.core.application.rdb.use_cases import (
    CreateCollectionUC,
    DeleteCollectionUC,
    GetAvailableCollectionsUC,
    GetCollectionUC,
    UpdateCollectionUC,
)
from app.src.infra.adapters.rdb.sqlalchemy.repository import SQLAlchemyRDBRepository
from dishka import Provider, Scope, provide


class CollectionUseCasesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_get_available_collections_uc(
        self, rdb_repo: SQLAlchemyRDBRepository
    ) -> GetAvailableCollectionsUC:
        return GetAvailableCollectionsUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_create_collection_uc(
        self, rdb_repo: SQLAlchemyRDBRepository
    ) -> CreateCollectionUC:
        return CreateCollectionUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_update_collection_uc(
        self, rdb_repo: SQLAlchemyRDBRepository
    ) -> UpdateCollectionUC:
        return UpdateCollectionUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_delete_collection_uc(
        self, rdb_repo: SQLAlchemyRDBRepository
    ) -> DeleteCollectionUC:
        return DeleteCollectionUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_collection_uc(
        self, rdb_repo: SQLAlchemyRDBRepository
    ) -> GetCollectionUC:
        return GetCollectionUC(rdb_repo)
