import scrapy


class SmartphoneItem(scrapy.Item):
    os_version = scrapy.Field()
    counter = scrapy.Field()
