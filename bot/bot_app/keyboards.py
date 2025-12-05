from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

return_button: InlineKeyboardButton = [InlineKeyboardButton(text="На главную",
                                                            callback_data="return")]

panels = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Открыть пользовательскую панель", callback_data='user_panel')],
    [InlineKeyboardButton(text="Открыть админ-панель", callback_data='admin_panel')]
], resize_keyboard=True)

user_actions = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отправить запрос", callback_data="user_query")],
    [InlineKeyboardButton(text="Найти документ", callback_data="find_document")],
    return_button
])

admin_actions = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Создать базу данных", callback_data="create_db")],
    [InlineKeyboardButton(text="Удалить базу данных", callback_data="delete_db")],
    [InlineKeyboardButton(text="Посмотреть доступные базы данных", callback_data="view_dbs")],
    [InlineKeyboardButton(text="Добавить документ в базу данных", callback_data="add_document")],
    return_button
])