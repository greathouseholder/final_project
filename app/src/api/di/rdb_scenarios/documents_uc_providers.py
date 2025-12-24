from dishka import Provider, Scope, provide

from src.core.application.rdb.use_cases import (
    DeleteDocumentUC,
    GetAvailableDocumentsUC,
    GetDocumentUC,
    UpdateDocumentUC,
)
from src.infra.adapters.rdb.interface import RDBRepository


class DocumentUseCasesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_get_document_uc(
            self, rdb_repo: RDBRepository) -> GetDocumentUC:
        return GetDocumentUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_delete_document_uc(
            self, rdb_repo: RDBRepository) -> DeleteDocumentUC:
        return DeleteDocumentUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_update_document_uc(
            self, rdb_repo: RDBRepository) -> UpdateDocumentUC:
        return UpdateDocumentUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_available_documents_uc(
            self, rdb_repo: RDBRepository) -> GetAvailableDocumentsUC:
        return GetAvailableDocumentsUC(rdb_repo)
