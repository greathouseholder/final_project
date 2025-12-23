from typing import Dict
from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery

from config import PAYMENT_TOKEN
from . import server_handlers as sh
import bot_app.keyboards as kb

payment_router = Router()

@payment_router.callback_query(F.data == "payment")
async def pay(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    is_paid: bool = False
    is_paid_info: Dict = await sh.is_paid(callback.from_user.id)
    if "detail" in is_paid_info:
        await callback.message.answer(f"Ошибка: {is_paid_info.get('detail')}")
    else:
        is_paid = is_paid_info.get("is_paid")
    if is_paid:
        await callback.message.edit_text("Подписка уже оплачена!",
                                         reply_markup=kb.to_main_menu_button_keyboard)
    else:
        description: str = 'Оплатить'
        price = [LabeledPrice(label="Оплатить", amount=100 * 100)]
        if price:
            await bot.send_invoice(
                chat_id=callback.from_user.id,
                title='Покупка',
                description=description,
                payload='sub1',
                provider_token=PAYMENT_TOKEN,
                currency='rub',
                start_parameter='test',
                prices=price
            )

@payment_router.pre_checkout_query()
async def process_pre_checkout_query(query: PreCheckoutQuery, bot: Bot) -> None:
    await bot.answer_pre_checkout_query(query.id, ok=True)

@payment_router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    payload_to_message = {
        'sub1': 'Теперь вы можете делать сколь угодно много запросов!'
    }
    response = payload_to_message.get(message.successful_payment.invoice_payload, 'Оплата успешна!')
    detail = await sh.subscription(message.from_user.id)
    if detail:
        await message.answer(detail.get("detail"))
    await message.answer(response)
