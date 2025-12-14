#для создания клавиатур
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

#вернуться в меню выбора панелей
return_button: InlineKeyboardButton = [InlineKeyboardButton(text="На главную",
                                                            callback_data="return")]
return_button_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    return_button
])

select_dialogue: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Создать новый диалог", callback_data='create_dialogue')],
    [InlineKeyboardButton(text="Показать список существующих диалогов", callback_data="show_dialogues_list")],
    [InlineKeyboardButton(text="Посмотреть доступные коллекции", callback_data="view_dbs_names")],
    [InlineKeyboardButton(text="Открыть панели", callback_data="panels")]
])

panels: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Открыть пользовательскую панель", callback_data='user_panel')],
    [InlineKeyboardButton(text="Открыть админ-панель", callback_data='admin_panel')],
    return_button
])

user_actions: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отправить запрос", callback_data="user_query")],
    [InlineKeyboardButton(text="Найти документ", callback_data="find_document")],
    [InlineKeyboardButton(text="Посмотреть доступные коллекции", callback_data="view_dbs_names")],
    return_button
])

admin_actions: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Посмотреть информацию о коллекциях", callback_data="view_dbs")],
    [InlineKeyboardButton(text="Добавить новую коллекцию", callback_data="add_db")],
    [InlineKeyboardButton(text="Удалить коллекцию", callback_data="delete_db")],
    [InlineKeyboardButton(text="Добавить документ в базу данных", callback_data="add_document")],
    return_button
])
