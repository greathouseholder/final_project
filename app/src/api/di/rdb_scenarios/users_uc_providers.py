from dishka import Provider, Scope, provide

from src.core.application.rdb.use_cases.user import (
    CheckAdminUC,
    CheckPaymentUC,
    GetAttemptCountUC,
    GetTelegramIdUC,
    GetUserIdUC,
    RecordPaymentUC,
    RegisterUserUC,
)
from src.infra.adapters.rdb.interface import RDBRepository


class UserUseCasesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_get_telegram_id_uc(
            self, rdb_repo: RDBRepository) -> GetTelegramIdUC:
        return GetTelegramIdUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_check_admin_uc(
            self, rdb_repo: RDBRepository) -> CheckAdminUC:
        return CheckAdminUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_user_id_uc(
            self, rdb_repo: RDBRepository) -> GetUserIdUC:
        return GetUserIdUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_attempt_count_uc(
            self, rdb_repo: RDBRepository) -> GetAttemptCountUC:
        return GetAttemptCountUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_chech_payment_uc(
            self, rdb_repo: RDBRepository) -> CheckPaymentUC:
        return CheckPaymentUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_record_payment_uc(
            self, rdb_repo: RDBRepository) -> RecordPaymentUC:
        return RecordPaymentUC(rdb_repo)

    @provide(scope=Scope.REQUEST)
    def provide_register_user_uc(
            self, rdb_repo: RDBRepository) -> RegisterUserUC:
        return RegisterUserUC(rdb_repo)
