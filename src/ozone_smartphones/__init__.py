from scrapy.http import Request


class ScrollableRequest(Request):
    """
    Adds parameters Scrapy's Request to handle page scrolling and load timeout
    :param timeout: page load timeout in seconds
    :param callback: if True, bot will scroll page
    """
    def __init__(self, timeout: int = 0, scroll_page: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.timeout = timeout
        self.scroll_page = scroll_page
