# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from random import choice

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class MeeshoSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class MeeshoDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        pxs = [
            "185.188.76.152",
            "104.249.0.116",
            "185.207.96.76",
            "185.205.197.4",
            "185.199.117.103",
            "185.193.74.119",
            "185.188.79.150",
            "185.195.223.146",
            "181.177.78.203",
            "185.207.98.115",
            "186.179.10.253",
            "185.196.189.131",
            "185.205.199.143",
            "185.195.222.22",
            "186.179.20.88",
            "185.188.79.126",
            "185.195.213.198",
            "185.207.98.192",
            "186.179.27.166",
            "181.177.73.165",
            "181.177.64.160",
            "104.233.53.55",
            "185.205.197.152",
            "185.207.98.200",
            "67.227.124.192",
            "104.249.3.200",
            "104.239.114.248",
            "181.177.67.28",
            "185.193.74.7",
            "216.10.5.35",
            "104.233.55.126",
            "185.195.214.89",
            "216.10.1.63",
            "104.249.1.161",
            "186.179.27.91",
            "185.193.75.26",
            "185.195.220.100",
            "185.205.196.226",
            "185.195.221.9",
            "199.168.120.156",
            "181.177.69.174",
            "185.207.98.8",
            "185.195.212.240",
            "186.179.25.90",
            "199.168.121.162",
            "185.199.119.243",
            "181.177.73.168",
            "199.168.121.239",
            "185.195.214.176",
            "181.177.71.233",
            "104.233.55.230",
            "104.249.6.234",
            "104.249.3.87",
            "67.227.125.5",
            "104.249.2.53",
            "181.177.64.15",
            "104.249.7.79",
            "186.179.4.120",
            "67.227.120.39",
            "181.177.68.19",
            "186.179.12.120",
            "104.233.52.54",
            "104.239.117.252",
            "181.177.77.65",
            "185.195.223.56",
            "185.207.99.39",
            "104.249.7.103",
            "185.207.99.11",
            "186.179.3.220",
            "181.177.72.117",
            "185.205.196.180",
            "104.249.2.172",
            "185.207.98.181",
            "185.205.196.255",
            "104.239.113.239",
            "216.10.1.94",
            "181.177.77.2",
            "104.249.6.84",
            "104.239.115.50",
            "185.199.118.209",
            "104.233.55.92",
            "185.207.99.117",
            "104.233.54.71",
            "185.199.119.25",
            "181.177.78.82",
            "104.239.113.76",
            "216.10.7.90",
            "181.177.78.202",
            "104.239.119.189",
            "181.177.64.245",
            "185.199.118.216",
            "185.199.116.219",
            "185.188.77.64",
            "185.199.116.185",
            "185.188.78.176",
            "186.179.12.162",
            "185.205.197.193",
            "181.177.74.161",
            "67.227.126.121",
            "181.177.79.185",

        ]

        # request.meta['proxy'] = f"http://kunal_santani577-9elgt:QyqTV6XOSp@{choice(pxs)}:3199"
        request.meta['proxy'] = "http://9dbe950ef6284a5da9e7749db9f7cbd1:@api.zyte.com:8011/"
        # request.meta['proxy'] = "http://scraperapi:de51e4aafe704395654a32ba0a14494d@proxy-server.scraperapi.com:8001"

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
