import scrapy
import json
import os
import random
import time
from datetime import datetime,timedelta
from typing import Iterable, Optional, Any, Union
import dateparser
import pymysql
import scrapy
from scrapy import Request, Spider
from scrapy.cmdline import execute
from twisted.internet.defer import Deferred
from meesho.items import *

import meesho.db_config as db


class MeeshoPinDataFinalSpider(scrapy.Spider):
    name = "meesho_pin_data_final"
    allowed_domains = ["meesho.com"]
    start_urls = ["https://meesho.com"]
    handle_httpstatus_list = [500, 520, 410, 400, 401, 521]
    oos_list = list()
    cookies_folder = "C:/Meesho/cookies"
    page_save_root = "C:/Meesho/"
    custom_settings = {
        "CONCURRENT_REQUESTS": 16,
        "REFERER_ENABLED": False,
    }
    DATE = str(datetime.now().strftime("%Y%m%d"))
    def __init__(self, name: Optional[str] = None, pincode: str = "560001",dbname=DATE, start=0, end=100000, **kwargs: Any):
        # def __init__(self, name: Optional[str] = None, pincode: str = "560001",dbname='20240918', start=0, end=100000, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.start = start
        self.end = end
        self.pincode = str(pincode).strip()
        self.pincode_city = {
            "560001": "BANGALORE",
            "110001": "DELHI",
            "400001": "MUMBAI",
            "700020": "KOLKATA",
            "212011": "Varanasi",
        }
        self.timestamp = dbname
        self.past_timestamp = '20240909'
        self.run_type = "master" if "master" in db.db_name else "normal"

        if db.db_name == "sy_meesho":
            self.page_save_root = f"C:/sy_Meesho/"

        self.folder_location = f"{self.page_save_root}pages_{self.run_type}/{self.timestamp}/new_task_html/"
        self.pincode_folder_location = f"{self.page_save_root}pages_{self.run_type}/{self.past_timestamp}/login_json_{pincode}/"
        os.makedirs(self.pincode_folder_location, exist_ok=True)
        self.oos_file = f"{self.page_save_root}pages_{self.run_type}/oos_{pincode}.txt"

        # DATABASE CONNECTION
        db.db_links_table = f'product_links_{dbname}'
        self.con = pymysql.connect(host=db.db_host, user=db.db_user, password=db.db_password, db=db.db_name)
        self.con.autocommit(True)
        self.cursor = self.con.cursor()

    def start_requests(self) -> Iterable[Request]:

        pincode_cookies = list()
        pincode_cookies.extend(json.loads(open(f"{self.cookies_folder}/all_cookies.json").read()))

        random.shuffle(pincode_cookies)

        oos_products = list()
        if os.path.exists(self.oos_file):
            oos_products = open(self.oos_file).readlines()

        count = 0

        for i in os.listdir(self.pincode_folder_location):
            name_list = i.rsplit(".", 1)[0].split("_")
            file_path = f'{self.pincode_folder_location}{name_list[0]}_{name_list[1]}.json'
            if os.path.exists(file_path):
                yield scrapy.Request(
                    url=f'file:///{file_path}',
                    cb_kwargs={
                        "i": i,
                        "name_list": name_list,
                        "retry_410": 0,
                        "retry_401": 0,
                        "file_path": file_path
                    },
                    dont_filter=True,
                )
                count += 1

    def parse(self, response,**kwargs):
        print(response.text)
        name_list = kwargs['name_list']
        product_id = name_list[0]
        supplier_id = name_list[1]
        file_path = kwargs['file_path']

        delivery_data = json.load(open(file_path))['shipping']
        past = False
        if 'estimated_delivery_date' in delivery_data:
            item = MeeshoItemPCdata()
            estimated_delivery_date = delivery_data['estimated_delivery_date']

            ###
            # Comment this code block  when done reading past data
            days_add = [59, 60]
            if past:
                tmp_arrival = dateparser.parse(
                    estimated_delivery_date.lower().split("by")[-1], settings={'DATE_ORDER': 'DMY'}
                ) + timedelta(days=random.choice(days_add))
                estimated_delivery_date = f"Estimated delivery by {self.format_datetime(tmp_arrival)}"
                print('Delivery date modified ', estimated_delivery_date)
            ###
            print(estimated_delivery_date)
            item['SKU_id_MEESHO'] = product_id
            item['Pincode'] = self.pincode
            item['City'] = self.pincode_city[self.pincode]
            item['Delivery_Date_MEESHO'] = estimated_delivery_date
            item['No_Delivery_Days_from_Scrape_Date_MEESHO'] = self.get_date(estimated_delivery_date)
            # item['Price_in_Cart__After_Applying_Coupon_MEESHO'] = product_price + data['shipping']['charges']
            yield item

    def retry_on_gt_400(self, response, meesho_pid, **kwargs):
        status_code = response.status
        if kwargs[f'retry_{status_code}'] > 3:
            update_query = f"update {db.db_links_table} set `status_{self.pincode}` = '{status_code}' where `meesho_pid` = '{meesho_pid}';"
            print(update_query)
            self.cursor.execute(update_query)
            return None
        else:
            kwargs[f'retry_{status_code}'] += 1
            requests: scrapy.Request = response.request.copy()
            requests.dont_filter = True
            requests.cb_kwargs.update(**kwargs)
            return requests

    def get_day_suffix(self,day):
        if 4 <= day <= 20 or 24 <= day <= 30:
            return "th"
        else:
            return ["st", "nd", "rd"][day % 10 - 1]
    def format_datetime(self,dt):
        day = dt.day
        suffix = self.get_day_suffix(day)
        formatted_date = dt.strftime(f"%A, {day}{suffix} %b")
        return formatted_date

    def get_date(self,string_obj, difference=0):
        arrival = dateparser.parse(string_obj.lower().split("by")[-1], settings={'DATE_ORDER': 'DMY'})
        return (arrival - datetime.now()).days


if __name__ == '__main__':
    pass
    execute("scrapy crawl meesho_pin_data_final -a pincode=400001 -a start=10514 -a end=10514".split())
