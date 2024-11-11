from scrapy import cmdline


def main():
    cmdline.execute("scrapy crawl Smartphone -o out.json".split())


if __name__ == "__main__":
    main()