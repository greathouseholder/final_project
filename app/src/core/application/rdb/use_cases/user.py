from uuid import UUID

from app.src.core.domain.rdb_entities import User


class CheckAdminUC:
    def __init__(self, rdb_repo):  # DI: RDBRepository
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
