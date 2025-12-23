from app.src.core.application.rdb.use_cases import (
    DeleteDocumentUC,
    GetAvailableDocumentsUC,
    GetDocumentUC,
    UpdateDocumentUC,
)
from app.src.infra.adapters.rdb.sqlalchemy.repository import SQLAlchemyRDBRepository
from dishka import Provider, Scope, provide


class DocumentUseCasesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_get_document_uc(
            self, rdb_repo: SQLAlchemyRDBRepository) -> GetDocumentUC:
        return GetDocumentUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_delete_document_uc(
            self, rdb_repo: SQLAlchemyRDBRepository) -> DeleteDocumentUC:
        return DeleteDocumentUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_update_document_uc(
            self, rdb_repo: SQLAlchemyRDBRepository) -> UpdateDocumentUC:
        return UpdateDocumentUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_available_documents_uc(
            self, rdb_repo: SQLAlchemyRDBRepository) -> GetAvailableDocumentsUC:
        return GetAvailableDocumentsUC(rdb_repo)
