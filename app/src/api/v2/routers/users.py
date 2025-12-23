from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, status

from src.api.v2.exceptions import handle_exception
from src.core.application.rdb.use_cases.user import CheckPaymentUC, GetUserIdUC, RecordPaymentUC

router = APIRouter(tags=["users"])


@router.post("/users/payment", status_code=status.HTTP_202_ACCEPTED)
@inject
async def record_payment(
    telegram_id: int,
    get_user_id_uc: FromDishka[GetUserIdUC],
    record_payment_uc: FromDishka[RecordPaymentUC]
):
    try:
        user_id: UUID = await get_user_id_uc.execute(telegram_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Регистрация пользователей не реализована"
        ) from None

    try:
        record_payment_uc.execute(user_id)
    except Exception as exc:
        return handle_exception(exc)


@router.get("/users/payment", status_code=status.HTTP_200_OK)
@inject
async def check_payment(
    telegram_id: int,
    get_user_id_uc: FromDishka[GetUserIdUC],
    check_payment_uc: FromDishka[CheckPaymentUC]
):
    try:
        user_id: UUID = await get_user_id_uc.execute(telegram_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Регистрация пользователей не реализована"
        ) from None

    try:
        is_paid: bool = check_payment_uc.execute(user_id)
    except Exception as exc:
        return handle_exception(exc)

    return {
        "is_paid": is_paid
    }
