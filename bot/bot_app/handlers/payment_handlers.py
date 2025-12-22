from typing import Dict
from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.context import FSMContext

from config import PAYMENT_TOKEN
from . import server_handlers as sh
import bot_app.keyboards as kb
from bot_app import states as st

payment_router = Router()

@payment_router.callback_query(F.data == "payment")
async def pay(callback: CallbackQuery, bot: Bot):
    await callback.answer()
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
    await message.answer(response)
    