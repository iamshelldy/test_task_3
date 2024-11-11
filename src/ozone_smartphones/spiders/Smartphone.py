from queue import Queue
from random import random

import pandas as pd
from scrapy import Spider, signals
from scrapy.selector import Selector

from ozone_smartphones import ScrollableRequest
from ozone_smartphones.items import SmartphoneItem


class SmartphoneSpider(Spider):
    name = "Smartphone"
    allowed_domains = ["ozon.ru"]
    start_urls = [f"https://www.ozon.ru/category/smartfony-15502/?sorting=rating"]
    products_urls = Queue()
    os_data = []

    def start_requests(self):
        yield ScrollableRequest(url=self.start_urls[0], callback=self.collect_products_urls, timeout=10)

    def collect_products_urls(self, response):
        root = Selector(response)

        counter = 0
        for i in range(1, 10):
            if counter == self.settings["NUMBER_OF_ITEMS_TO_COLLECT"]:
                break

            for j in range(1, 13):
                if counter == self.settings["NUMBER_OF_ITEMS_TO_COLLECT"]:
                    break
                product_link_obj = root.xpath(f"//*[@id='paginatorContent']/div[{i}]/div/div[{j}]/div/div[1]/a")
                product_link = product_link_obj.xpath("@href").get().split("?")[0]
                self.products_urls.put("https://www." + self.allowed_domains[0] + product_link + "features/")
                counter += 1

        while not self.products_urls.empty():
            current_url = self.products_urls.get()
            yield ScrollableRequest(url=current_url, callback=self.collect_products_infos,
                                    timeout=1+random(), scroll_page=False)

    def collect_products_infos(self, response):
        root = Selector(response)
        main_infos_block = root.xpath(f"//div[contains(text(), '{self.settings["MAIN_INFO_BLOCK"]}')]"
                                      "/following-sibling::div[last()]/dl[last()]")

        main_infos_rows = main_infos_block.xpath(".//dd/text()").getall()
        if len(main_infos_rows) == 0:
            main_infos_rows = main_infos_block.xpath(".//dd/a/text()").getall()

        os_version = self.clean_os_data(main_infos_rows[-1])
        self.os_data.append(os_version)

        if len(self.os_data) == self.settings["NUMBER_OF_ITEMS_TO_COLLECT"]:
            result_data = pd.DataFrame(self.os_data, columns=["os_version"])
            result_data = result_data["os_version"].value_counts().to_dict()

            for key in result_data:
                print(f"{key} - {result_data[key]}")
                yield SmartphoneItem({"os_version": key, "counter": result_data[key]})

    @staticmethod
    def clean_os_data(os_string: str) -> str:
        replace_rules = {".x": "", ".х": "", ".0": ""}
        for key, value in replace_rules.items():
            os_string = os_string.replace(key, value)

        if " " not in os_string:
            os_string += " Unknown"

        return os_string
