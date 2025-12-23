from app.src.core.application.rdb.use_cases.user import (
    CheckAdminUC,
    CheckPaymentUC,
    GetAttemptCountUC,
    GetTelegramIdUC,
    GetUserIdUC,
    RecordPaymentUC,
)
from app.src.infra.adapters.rdb.sqlalchemy.repository import SQLAlchemyRDBRepository
from dishka import Provider, Scope, provide


class UserUseCasesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_get_telegram_id_uc(
            self, rdb_repo: SQLAlchemyRDBRepository) -> GetTelegramIdUC:
        return GetTelegramIdUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_check_admin_uc(
            self, rdb_repo: SQLAlchemyRDBRepository) -> CheckAdminUC:
        return CheckAdminUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_user_id_uc(
            self, rdb_repo: SQLAlchemyRDBRepository) -> GetUserIdUC:
        return GetUserIdUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_attempt_count_uc(
            self, rdb_repo: SQLAlchemyRDBRepository) -> GetAttemptCountUC:
        return GetAttemptCountUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_chech_payment_uc(
            self, rdb_repo: SQLAlchemyRDBRepository) -> CheckPaymentUC:
        return CheckPaymentUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_record_payment_uc(
            self, rdb_repo: SQLAlchemyRDBRepository) -> RecordPaymentUC:
        return RecordPaymentUC(rdb_repo)
