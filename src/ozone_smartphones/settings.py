BOT_NAME = "ozone_smartphones"

SPIDER_MODULES = ["ozone_smartphones.spiders"]

ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
   "ozone_smartphones.middlewares.SeleniumMiddleware": 1,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

LOG_LEVEL = "WARNING"

# Uncomment to use en locale
# LOCALE = ["en-US", "en"]
# MAIN_INFO_BLOCK = "Main"

# Uncomment to use ru locale
LOCALE = ["ru-RU", "ru"]
MAIN_INFO_BLOCK = "Основные"

NUMBER_OF_ITEMS_TO_COLLECT = 100
