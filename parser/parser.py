import logging
import schedule

from bs4 import BeautifulSoup

from utils import create_driver, add_to_file, next_page, delay
from config import URL

products_count = 0
pages = 0


def parse_page(driver) -> list:
    global products_count, pages

    soup = BeautifulSoup(driver.page_source, "lxml")
    products = soup.find_all("div", class_="item-block")

    to_add = []
    for product in products:
        name = product.find("div", class_="item-title").text.replace("\n", "").replace("\t", "").replace("  ", "")
        link = "https://megamarket.ru" + product.find("a", class_="ddl_product_link").get("href")
        price = product.find("div", class_="item-price").text.replace("₽", "").replace(" ", "")
        bonus = product.find_all("span", class_="bonus-amount")
        if bonus:
            bonus = bonus[0].text.replace(" ", "")
            b = int(round(int(bonus) / int(price), 2) * 100)
            s = f"{name} | {price} | {b} | {link}"
            to_add.append(s)
    products_count += len(to_add)
    pages += 1
    logging.info(f"{pages} pages has been added ({products_count} products)")
    return to_add


def parser() -> None:
    driver = create_driver()
    driver.get(URL)
    number_of_pages = 200
    data_to_write = []
    for i in range(number_of_pages):
        for j in range(3):
            try:
                to_add = parse_page(driver)
                data_to_write.extend(to_add)
                break
            except:
                driver.refresh()
                delay()
        try:
            is_alive = next_page(driver)
            delay()
            if not is_alive:
                driver.close()
                add_to_file("products.txt", data_to_write)
                return
        except:
            driver.refresh()
            delay()
    add_to_file("products.txt", data_to_write)


def main() -> None:
    global pages, products_count
    logging.info("start working")
    parser()
    logging.info("end working")
    logging.info("-" * 20)
    products_count = 0
    pages = 0


def start_schedule() -> None:
    schedule.every().hour.at(":17").do(main)
    schedule.every().hour.at(":47").do(main)
    while True:
        schedule.run_pending()
        delay()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
    start_schedule()
