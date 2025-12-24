#для создания клавиатур
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отправить запрос", callback_data="RAG_query")],
    [InlineKeyboardButton(text="Поиск по документам", callback_data="search")],
    [InlineKeyboardButton(text="Коллекции", callback_data="collections")],
    [InlineKeyboardButton(text="Оплатить подписку", callback_data="pay")]
])

collections_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить коллекцию", callback_data="add_db")],
    [InlineKeyboardButton(text="Действия с коллекциями", callback_data="collections_actions")],
    [InlineKeyboardButton(text="Посмотреть полную информацию о коллекциях", callback_data="view_dbs")]
])

collections_actions_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Удалить документ из коллекции", callback_data="delete_doc")],
    [InlineKeyboardButton(text="Посмотреть документы", callback_data="view_docs")],
    [InlineKeyboardButton(text="Удалить коллекцию", callback_data="delete_db")],
    [InlineKeyboardButton(text="Добавить документ в коллекцию", callback_data="add_doc")],
    [InlineKeyboardButton(text="Изменить коллекцию", callback_data='update_coll')],
    [InlineKeyboardButton(text="Получить информацию о коллекции", callback_data='view_collection')]
])

number_of_sources = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="1", callback_data="sources_1"),
     InlineKeyboardButton(text="2", callback_data="sources_2"),
     InlineKeyboardButton(text="3", callback_data="sources_3"),
     InlineKeyboardButton(text="4", callback_data="sources_4"),
     InlineKeyboardButton(text="5", callback_data="sources_5")
     ],
     [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
])

is_public_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Публичная", callback_data="public_1"),
     InlineKeyboardButton(text="Приватная", callback_data="public_0")]
])

document_actions_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Посмотреть информацию о документе", callback_data="doc_info")],
    [InlineKeyboardButton(text="Изменить информацию о документе", callback_data="update_doc")]
])

payment_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Хочу", callback_data="payment"),
     InlineKeyboardButton(text="Не хочу", callback_data="main_menu")]
])

def create_pagination_keyboard(items: list,
                               item_type: str = "c",
                               page: int = 0,
                               items_per_page: int = 5) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    start = page * items_per_page
    end = start + items_per_page
    page_items = items[start:end]
    item_type_full = "collection" if item_type == "c" else "document"
    for item in page_items:
        _uuid = item.get(f'{item_type_full}_id')
        builder.button(
            text=f"{item.get('name', 'Без названия')[:30]}",
            callback_data=f"{item_type}:{str(_uuid)}"
        )

    builder.adjust(1) 
    
    navigation_cnt: int = 1

    if page > 0:
        builder.button(text="⬅️ Назад", callback_data=f"page_{page-1}")
        navigation_cnt += 1

    builder.button(text=f"📄 {page+1}/{((len(items)-1)//items_per_page)+1}",
                   callback_data="current_page")
    
    if end < len(items):
        builder.button(text="Вперед ➡️", callback_data=f"page_{page+1}")
        navigation_cnt += 1
    
    pattern = [1] * len(page_items) + [navigation_cnt, 1]
    builder.button(text="🏠 Главное меню", callback_data="main_menu")
    builder.adjust(*pattern)
    
    return builder.as_markup()

cancel_button_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
])

to_main_menu_button_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="В меню", callback_data="main_menu")]
])