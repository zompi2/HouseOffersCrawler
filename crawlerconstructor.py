# Constructs a crawler based on the given name

from crawlers.crawler_olx import CrawlerOlx

def ConstructCrawler(name):
    if name == "olx":
        return CrawlerOlx()
