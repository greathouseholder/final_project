from uuid import UUID

from fastapi import HTTPException, status

from src.api.v2.exceptions import handle_exception
from src.api.v2.schemas import BaseRequest
from src.core.application.rdb.use_cases.user import CheckAdminUC, RegisterUserUC


async def get_user_id(
    telegram_id: int | None,
    request_data: BaseRequest | None,
    register_user_uc: RegisterUserUC
) -> UUID:
    """
    Получить user_id по telegram_id из разных источников.
    """
    if telegram_id is not None:
        t_id = telegram_id
    elif request_data and request_data.telegram_id is not None:
        t_id = request_data.telegram_id
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не указан telegram_id"
        )

    try:
        return await register_user_uc.execute(t_id)
    except Exception as exc:
        raise handle_exception(exc) from exc


async def check_admin_rights(
    user_id: UUID,
    check_admin_uc: CheckAdminUC
):
    """
    Проверить, что пользователь - администратор.
    """
    if not await check_admin_uc.execute(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав на выполнение этого действия"
        )
