from ..items import ImagespiderItem
import scrapy

class ImageSpider(scrapy.Spider):
    name = "image-spider"
    start_urls = ["http://photography.nationalgeographic.com/photography/"]

    def parse(self, response):
        for href in response.css("a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_images)

    def parse_images(self, response):
        for src in response.css("img::attr('src')"):
            image_url = src.extract()
            if image_url.endswith("jpg"):
                yield {'url': response.url, 'image_url': image_url}
