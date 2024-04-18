from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import kb
from states import SettingsInput
from utils import create_message, parse_products

import config

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(f"Привет, это бот-парсер мегамаркета", reply_markup=kb.menu)
    print(msg.chat.id)


@router.message(F.text.lower() == "текущие настройки")
async def current_list_handler(message: Message):
    pmn = config.search_settings["price_min"]
    pmx = config.search_settings["price_max"]
    pname = config.search_settings["product_name"]
    cmn = config.search_settings["cashback_min"]
    if not pmn:
        pmn = "нет"
    if pmx == 1e10:
        pmx = "нет"
    if not cmn:
        cmn = "нет"
    if not pname:
        pname = "нет"
    await message.answer(f"Текущие настройки:\nТовар: {pname}\nМинимальная цена: {pmn}\n"
                         f"Максимальная цена: {pmx}\nМинимальный кэшбэк: {cmn}")


@router.message(F.text.lower() == "актуальный список")
async def current_list_handler(message: Message):
    await message.answer("Введите настройки поиска, после нажмите далее", reply_markup=kb.search_settings)


@router.callback_query(F.data)
async def search_settings_handler(callback: types.CallbackQuery, state: FSMContext):
    t = callback.data
    if t != "next":
        await callback.message.answer(f"Введите {kb.callback_to_text[t]}:")
        await state.set_state(SettingsInput.callback_to_state[t])
    else:
        products = parse_products("products.txt")
        messages_to_user = create_message(products)
        if not messages_to_user:
            await callback.message.answer("Товаров, подходящих под фильтр, сейчас нет")
        else:
            for message in messages_to_user:
                await callback.message.answer(message)
            await state.clear()


@router.message(StateFilter("*"))
async def add_setting_handler(msg: Message, state: FSMContext):
    cur_state = await state.get_state()
    cur_state = cur_state.split(":")[1]
    if cur_state == "product_name_input":
        if msg.text != "0":
            config.search_settings[SettingsInput.state_to_callback[cur_state]] = msg.text
            await msg.answer(f"Настройка добавлена")
        else:
            config.search_settings[SettingsInput.state_to_callback[cur_state]] = ""
            await msg.answer("Фильтр по названию удален")
    else:
        config.search_settings[SettingsInput.state_to_callback[cur_state]] = int(msg.text)
        await msg.answer(f"Настройка добавлена")
    await state.clear()
