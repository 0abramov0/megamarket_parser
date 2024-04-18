import os
import time

from selenium import webdriver as wd
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from config import TIMEOUT


def set_options() -> wd.ChromeOptions:
    options = wd.ChromeOptions()
    options.add_argument("start-maximized")
    # options.add_argument("headless")
    # options.page_load_strategy = "eager"
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    return options


def create_driver() -> wd.Chrome:
    driver = wd.Chrome(options=set_options())
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                                         'AppleWebKit/537.36 (KHTML, like '
                                                                         'Gecko)'
                                                                         'Chrome/83.0.4103.53 Safari/537.36'})
    return driver


def add_to_file(file_name: str, to_add: list) -> None:
    path = os.path.join(os.path.dirname(os.getcwd()), file_name)
    with open(path, "w", encoding="utf-8") as f:
        for line in to_add:
            f.write(line + "\n")


def next_page(driver: wd.Chrome) -> bool:
    i = 0
    while i < 3:
        try:
            WebDriverWait(driver, TIMEOUT).until(ec.visibility_of_element_located((By.CLASS_NAME, "next")))
            el = driver.find_element(By.CLASS_NAME, "next")
            next_page_button = el.find_element(By.TAG_NAME, "a")
            next_page_button.click()
            return True
        except TimeoutException:
            i += 1
    return False


def delay() -> None:
    time.sleep(TIMEOUT)
