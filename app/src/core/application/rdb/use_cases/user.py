from uuid import UUID

from src.core.domain.rdb_entities import User
from src.infra.adapters.rdb.interface import RDBRepository


class CheckAdminUC:
    def __init__(self, rdb_repo):
        self.rdb_repo = rdb_repo

    async def execute(self, telegram_id: int) -> bool:
        user = await self.rdb_repo.get_user_by_telegram_id(telegram_id)
        return user.role == "admin" if user else False


class GetUserIdUC:
    def __init__(self, rdb_repo):
        self.rdb_repo = rdb_repo

    async def execute(self, telegram_id: int) -> UUID:
        user = await self.rdb_repo.get_user_by_telegram_id(telegram_id)
        if not user:
            raise ValueError(f"User with telegram_id {telegram_id} not found")
        return user.user_id


class GetTelegramIdUC:
    def __init__(self, rdb_repo):
        self.rdb_repo = rdb_repo

    async def execute(self, user_id: UUID) -> int:
        user = await self.rdb_repo.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return user.telegram_id


class GetAttemptCountUC:
    def __init__(self, rdb_repo):
        self.rdb_repo = rdb_repo

    async def execute(self, user_id: UUID) -> int:
        user = await self.rdb_repo.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return user.attempt_count


class CheckPaymentUC:
    """Проверяет, является ли пользователь платящим (подписка активна)"""

    def __init__(self, rdb_repo):
        self.rdb_repo = rdb_repo

    async def execute(self, user_id: UUID) -> bool:
        user = await self.rdb_repo.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return user.is_paid


class RecordPaymentUC:
    """
    Отмечает пользователя как платящего.
    Обычно вызывается после успешной оплаты подписки.
    Можно также сбросить attempt_count, если это нужно по логике.
    """

    def __init__(self, rdb_repo):
        self.rdb_repo = rdb_repo

    async def execute(
            self, user_id: UUID, reset_attempts: bool = True) -> None:
        user = await self.rdb_repo.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        updates = {"is_paid": True}
        if reset_attempts:
            updates["attempt_count"] = 0

        await self.rdb_repo.update_user(user_id, **updates)

    class RegisterUserUC:
        """Автоматически регистрирует пользователя при первом обращении"""

        def __init__(self, rdb_repo: RDBRepository):
            self.rdb_repo = rdb_repo

        async def execute(self, telegram_id: int) -> User:
            user = await self.rdb_repo.get_user_by_telegram_id(telegram_id)
            if user:
                return user
            return await self.rdb_repo.create_user(
                telegram_id=telegram_id,
                role="user",
                is_paid=False,
                attempt_count=0
            )
