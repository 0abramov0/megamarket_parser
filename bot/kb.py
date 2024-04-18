from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

menu_buttons = [
    [KeyboardButton(text="Текущие настройки")],
    [KeyboardButton(text="Актуальный список")],
]

menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=menu_buttons)

search_settings_buttons = [
    [InlineKeyboardButton(text="Цена мин.", callback_data="price_min"), InlineKeyboardButton(text="Цена макс.", callback_data="price_max")],
    [InlineKeyboardButton(text="Кэшбэк мин.", callback_data="cashback_min"), InlineKeyboardButton(text="Название", callback_data="product_name")],
    [InlineKeyboardButton(text="Далее >>", callback_data="next")]
]

callback_to_text = {
    "price_min": "минимальную цену",
    "price_max": "максимальную цену",
    "cashback_min": "минимальный процент кэшбэка",
    "product_name": "название товара (введите 0, если хотите сбросить фильтр)",
}

search_settings = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=search_settings_buttons)
