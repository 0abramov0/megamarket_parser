from aiogram.filters.state import StatesGroup, State


class SettingsInput(StatesGroup):
    price_min_input = State()
    price_max_input = State()
    cashback_min_input = State()
    product_name_input = State()
    link_input = State()

    callback_to_state = {
        "price_min": price_min_input,
        "price_max": price_max_input,
        "cashback_min": cashback_min_input,
        "product_name": product_name_input,
    }
    state_to_callback = {
        "price_min_input": "price_min",
        "price_max_input": "price_max",
        "cashback_min_input": "cashback_min",
        "product_name_input": "product_name",
    }
