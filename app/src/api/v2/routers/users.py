from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from src.api.v2.exceptions import handle_exception
from src.api.v2.helpers import get_user_id
from src.core.application.rdb.use_cases.user import CheckPaymentUC, RecordPaymentUC, RegisterUserUC

router = APIRouter(tags=["users"])


@router.post("/users/payment", status_code=status.HTTP_200_OK)
@inject
async def record_payment(
    telegram_id: int,
    register_user_uc: FromDishka[RegisterUserUC],
    record_payment_uc: FromDishka[RecordPaymentUC]
):
    try:
        user_id = await get_user_id(telegram_id, None, register_user_uc)
        await record_payment_uc.execute(user_id)

    except Exception as exc:
        raise handle_exception(exc) from None


@router.get("/users/payment", status_code=status.HTTP_200_OK)
@inject
async def check_payment(
    telegram_id: int,
    register_user_uc: FromDishka[RegisterUserUC],
    check_payment_uc: FromDishka[CheckPaymentUC]
):
    try:
        user_id = await get_user_id(telegram_id, None, register_user_uc)
        is_paid: bool = await check_payment_uc.execute(user_id)
        return {"is_paid": is_paid}

    except Exception as exc:
        raise handle_exception(exc) from None
