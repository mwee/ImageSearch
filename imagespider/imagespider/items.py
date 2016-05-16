import scrapy

class ImagespiderItem(scrapy.Item):
    title = scrapy.Field()
    pubDate = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
