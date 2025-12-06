#для создания клавиатур
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

return_button: InlineKeyboardButton = [InlineKeyboardButton(text="На главную",
                                                            callback_data="return")]

return_button_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    return_button
])

panels: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Открыть пользовательскую панель", callback_data='user_panel')],
    [InlineKeyboardButton(text="Открыть админ-панель", callback_data='admin_panel')]
])

user_actions: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отправить запрос", callback_data="user_query")],
    [InlineKeyboardButton(text="Найти документ", callback_data="find_document")],
    [InlineKeyboardButton(text="Посмотреть доступные базы данных", callback_data="view_dbs_names")],
    return_button
])

admin_actions: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Посмотреть информацию о базах данных", callback_data="view_dbs")],
    [InlineKeyboardButton(text="Создать базу данных", callback_data="create_db")],
    [InlineKeyboardButton(text="Удалить базу данных", callback_data="delete_db")],
    [InlineKeyboardButton(text="Добавить документ в базу данных", callback_data="add_document")],
    return_button
])