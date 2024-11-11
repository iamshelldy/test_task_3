import time
from random import random

from scrapy import signals
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from scrapy.http import HtmlResponse

from ozone_smartphones import ScrollableRequest
from ozone_smartphones.settings import LOCALE


class SeleniumMiddleware:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("start-maximized")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    stealth(driver, languages=LOCALE, platform="Win64", fix_hairline=True)

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        if not isinstance(request, ScrollableRequest):
            return None

        self.driver.get(request.url)

        for (cookie_name, cookie_value) in request.cookies.items():
            self.driver.add_cookie({"name": cookie_name, "value": cookie_value})

        time.sleep(request.timeout)

        if request.scroll_page:
            body_element = self.driver.find_element(By.TAG_NAME, "body")

            # On ozon products are grouped by 4 items in one row
            # So we need to know how many times we need to scroll the page
            if spider.settings["NUMBER_OF_ITEMS_TO_COLLECT"] % 4 == 0:
                # Decrease by 1 cause if we want to proceed 1 row, we don't need to scroll page
                scroll_counter = spider.settings["NUMBER_OF_ITEMS_TO_COLLECT"] // 4 - 1
            else:
                # Scroll by a non-integer number from 0 to 1 times is equivalent to 1 time
                scroll_counter = spider.settings["NUMBER_OF_ITEMS_TO_COLLECT"] // 4

            for i in range(scroll_counter):
                body_element.send_keys(Keys.PAGE_DOWN)
                time.sleep(1.5 + random())

        body = self.driver.page_source.encode()

        return HtmlResponse(
            self.driver.current_url,
            body=body,
            encoding="utf-8",
            request=request
        )

    def spider_closed(self):
        self.driver.close()
        self.driver.quit()
