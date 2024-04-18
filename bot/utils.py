import os

from aiogram import Bot

from config import CHAT_ID, search_settings, NUMBER_OF_PRODUCT


def parse_products(file_name: str) -> list:
    path = os.path.join(os.path.dirname(os.getcwd()), file_name)
    with open(path, "r", encoding="utf-8") as f:
        r = f.read().split("\n")

    data = []
    for line in r:
        if line:
            data.append(line.split(" | "))
    data = list(filter(lambda x: search_settings["price_max"] >= int(x[1]) >= search_settings["price_min"] and int(x[2]) >= search_settings["cashback_min"] and search_settings["product_name"] in x[0].lower(), data))
    data.sort(key=lambda x: int(x[2]), reverse=True)
    data = data[:NUMBER_OF_PRODUCT]
    return data


def create_message(data: list) -> list:
    msg = ""
    msg_lst = []
    for i in range(len(data)):
        if len(data[i]) < 4:
            continue
        name, price, bonus, link = data[i][0], data[i][1], data[i][2], data[i][3]
        msg += f"Название: {name}\n"
        msg += f"Цена: {price}\n"
        msg += f"Кэшбэк: {bonus}%\n"
        msg += f"Ссылка: {link}\n"
        msg += "-" * 50 + "\n"
        if msg and i and i % 10 == 0:
            msg_lst.append(msg)
            msg = ""
    if msg:
        msg_lst.append(msg)
    return msg_lst


async def send_by_timer(bot: Bot):
    products = parse_products("products.txt")
    messages_to_user = create_message(products)
    if not messages_to_user:
        await bot.send_message(CHAT_ID, "Товаров, подходящих под фильтр, сейчас нет")
    else:
        for message in messages_to_user:
            await bot.send_message(CHAT_ID, message)
