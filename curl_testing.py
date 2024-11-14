import scrapy


class CurlTestingSpider(scrapy.Spider):
    name = "curl_testing"
    allowed_domains = ["www.meesho.com"]
    start_urls = ["https://www.meesho.com"]

    def parse(self, response):
        pass
