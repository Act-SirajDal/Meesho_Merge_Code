import json
import os
import random
import time
from datetime import datetime, timedelta
from typing import Iterable

import pymysql
import scrapy
from scrapy import Request, Spider
from scrapy.cmdline import execute
import meesho.db_config as db


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["meesho.com"]
    start_urls = ["https://meesho.com"]
    handle_httpstatus_list = [403, 429, 400]
    folder_location = f"D:/Meesho/"
    errors = list()
    # custom_settings = {
    #     "DOWNLOAD_HANDLERS": {
    #         "http": "scrapy_impersonate.ImpersonateDownloadHandler",
    #         "https": "scrapy_impersonate.ImpersonateDownloadHandler",
    #     },
    #     "DOWNLOADER_MIDDLEWARES": None
    # }

    DATE = str(datetime.now().strftime("%Y%m%d"))
    # DATE = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")
    # DATE = '20241106'
    def __init__(self, name=None, start=0, end=100000, dbname=DATE, **kwargs):
    # def __init__(self, name=None, start=0, end=100000, dbname='20241008', **kwargs):
        super().__init__(name, **kwargs)
        # DATABASE SPECIFIC VALUES
        self.start = start
        self.end = end
        # db.db_name = 'meesho_master'
        db.db_links_table = f'product_links_{dbname}'
        self.timestamp = dbname
        self.run_type = "master" if "master" in db.db_name else "normal"

        if db.db_name == "sy_meesho":
            self.folder_location = f"D:/sy_Meesho/"

        self.folder_location = self.folder_location + f"pages_{self.run_type}/{self.timestamp}/new_task_html/"

        os.makedirs(self.folder_location, exist_ok=True)

        # DATABASE CONNECTION
        self.con = pymysql.connect(host=db.db_host, user=db.db_user, password=db.db_password, db=db.db_name)
        self.con.autocommit(True)
        self.cursor = self.con.cursor()

    def start_requests(self) -> Iterable[Request]:

        query = f"select `meesho_pid` FROM {db.db_links_table} where status='pending' and id between {self.start} and {self.end} limit 200;"
        self.cursor.execute(query)
        query_results = self.cursor.fetchall()
        self.logger.info(f"\n\n\nTotal Results ...{len(query_results)}\n\n\n", )

        processed_pid = [i.split("_")[0].lower() for i in os.listdir(self.folder_location)]

        for i in query_results:
            if not i[0]:
                continue
            i = i[0].strip()
            # i = "19vdbx"

            # if i in processed_pid:
                # update_query = f"update {db.db_links_table} set `status` = 'Done' where `meesho_pid` = '{i}'"
                # print(update_query)
                # self.cursor.execute(update_query)
                # self.con.commit()
                # continue

            if not os.path.exists(self.folder_location + i + ".html"):
                url = "https://www.meesho.com/s/p/" + i

                yield scrapy.Request(
                    url=url,
                    cb_kwargs={
                        "page_name": i
                    },
                    meta={"impersonate": random.choice(["chrome110", "edge99", "safari15_5"])},
                )

    def parse(self, response, **kwargs):

        if response.status in [403, 429]:
            request = response.request.copy()
            request.meta.update({"impersonate": random.choice(["chrome110", "edge99", "safari15_5"])})
            request.dont_filter = True
            yield request
            return None

        i = kwargs['page_name']

        try:
            status = "Done"
            data = response.body.split(b'id="__NEXT_DATA__" type="application/json">')[1].split(b"</script>")[0]
            data = json.loads(data)['props']['pageProps']['initialState']['product']['details']['data']
            if data:
                if data['valid']:
                    if 'suppliers' not in data:
                        return None
                    supplier = data['suppliers'][0]
                    supplier_name = str(supplier['id'])

                    # supplier_listed_product_count = 0
                    # for shop_value_prop in supplier['shop_value_props']:
                    #     if 'product' in shop_value_prop:
                    #         supplier_listed_product_count = shop_value_prop['product']['count']
                    #         break
                    # if not supplier_listed_product_count:
                    #     status = "Zero Product Seller"

                    open(self.folder_location + i + f"_{supplier_name}.html", "wb").write(response.body)
                else:
                    status = "This product is out of stock"
            else:
                status = "Not Found page"

            # TODO: DON'T UNCOMMENT THIS UNTIL GET CONFIRMATION FROM DEEP
            # if f'"in_stock":false,"product_id":"{i}"':
            #     status = "Out of Stock while add to cart"

            update_query = f"update {db.db_links_table} set `status` = '{status}' where `meesho_pid` = '{i}'"
            # print(update_query)
            self.cursor.execute(update_query)
        except Exception as e:
            print(i, e)
            self.errors.append(i)


if __name__ == '__main__':
    pass
    execute('scrapy crawl products -a start=1 -a end=1000000'.split())

    # for i in range(80):
    #     print(i)
    #     os.system('taskkill /F /FI "WindowTitle eq meesho_product_*"')
    #     os.system('start "meesho_product_10000" scrapy crawl products -a start=00001 -a end=10000 -a dbname=20240703')
    #     os.system('start "meesho_product_20000" scrapy crawl products -a start=10001 -a end=20000 -a dbname=20240703')
    #     os.system('start "meesho_product_30000" scrapy crawl products -a start=20001 -a end=30000 -a dbname=20240703')
    #     os.system('start "meesho_product_40000" scrapy crawl products -a start=30001 -a end=40000 -a dbname=20240703')
    #     os.system('start "meesho_product_50000" scrapy crawl products -a start=40001 -a end=50000 -a dbname=20240703')
    #     os.system('start "meesho_product_60000" scrapy crawl products -a start=50001 -a end=60000 -a dbname=20240703')
    #     os.system('start "meesho_product_70000" scrapy crawl products -a start=60001 -a end=70000 -a dbname=20240703')
    #     os.system('start "meesho_product_80000" scrapy crawl products -a start=70001 -a end=80000 -a dbname=20240703')
    #     os.system('start "meesho_product_90000" scrapy crawl products -a start=80001 -a end=90000 -a dbname=20240703')
    #     os.system('start "meesho_product_99999" scrapy crawl products -a start=90001 -a end=99999 -a dbname=20240703')
    #     time.sleep(45)
