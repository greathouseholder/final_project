from dishka import Provider, Scope, provide

from src.core.application.rdb.use_cases import (
    CreateCollectionUC,
    DeleteCollectionUC,
    GetAvailableCollectionsUC,
    GetCollectionUC,
    UpdateCollectionUC,
)
from src.infra.adapters.rdb.interface import RDBRepository


class CollectionUseCasesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_get_available_collections_uc(
        self, rdb_repo: RDBRepository
    ) -> GetAvailableCollectionsUC:
        return GetAvailableCollectionsUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_create_collection_uc(
        self, rdb_repo: RDBRepository
    ) -> CreateCollectionUC:
        return CreateCollectionUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_update_collection_uc(
        self, rdb_repo: RDBRepository
    ) -> UpdateCollectionUC:
        return UpdateCollectionUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_delete_collection_uc(
        self, rdb_repo: RDBRepository
    ) -> DeleteCollectionUC:
        return DeleteCollectionUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_collection_uc(
        self, rdb_repo: RDBRepository
    ) -> GetCollectionUC:
        return GetCollectionUC(rdb_repo)
