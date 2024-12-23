import requests
import json
import os
import random
import time
import dateparser
from datetime import datetime, timedelta
from typing import Iterable
from meesho.items import *
import pymysql
import scrapy
from scrapy import Request, Spider
from scrapy.cmdline import execute
import meesho.db_config as db
from PIL import ImageFile


class MeeshoFSpider(scrapy.Spider):
    name = "meesho_pro_data_final"
    allowed_domains = ["meesho.com"]
    start_urls = ["https://meesho.com"]
    handle_httpstatus_list = [403, 429, 400]
    folder_location = f"C:/Meesho/"
    errors = list()

    DATE = str(datetime.now().strftime("%Y%m%d"))

    def __init__(self, name=None, start=0, end=100000, dbname=DATE, **kwargs):
        super().__init__(name, **kwargs)
        # DATABASE SPECIFIC VALUES
        self.start = start
        self.end = end
        db.db_links_table = f'product_links_{dbname}'
        self.timestamp = dbname
        self.past_timestamp = "20240909"
        self.run_type = "master" if "master" in db.db_name else "normal"

        if db.db_name == "sy_meesho":
            self.folder_location = f"C:/sy_Meesho/"

        self.folder_location = self.folder_location + f"pages_{self.run_type}/{self.timestamp}/new_task_html/"

        os.makedirs(self.folder_location, exist_ok=True)
        os.makedirs(f'{self.folder_location}/image', exist_ok=True)

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

            if not os.path.exists(self.folder_location + i + ".html"):
                url = "https://www.meesho.com/s/p/" + i

                yield scrapy.Request(
                    url=url,
                    cb_kwargs={
                        "page_name": i
                    },
                    meta={"impersonate": random.choice(["chrome110", "edge99", "safari15_5"])},
                )
            # break

    def parse(self, response, **kwargs):

        if response.status in [403, 429]:
            request = response.request.copy()
            request.meta.update({"impersonate": random.choice(["chrome110", "edge99", "safari15_5"])})
            request.dont_filter = True
            yield request
            return None

        i = kwargs['page_name']

        status = "Done"
        data = response.body.split(b'id="__NEXT_DATA__" type="application/json">')[1].split(b"</script>")[0]
        data = json.loads(data)['props']['pageProps']['initialState']['product']['details']['data']

        if data:
            if data['valid']:
                if 'suppliers' not in data:
                    return None
                supplier = data['suppliers'][0]
                supplier_name = str(supplier['id'])

                open(self.folder_location + i + f"_{supplier_name}.html", "wb").write(response.body)
                page = open(self.folder_location + i + f"_{supplier_name}.html", "rb").read()
                pincode_city = {
                    # "560001": "BANGALORE",
                    # "110001": "DELHI",
                    "400001": "MUMBAI",
                    # "700020": "KOLKATA",
                    # "212011": "Varanasi",
                }

                final_data = list()

                for pincode in pincode_city.keys():
                    print("=" * 20, pincode, "=" * 20)

                    if data:
                        product_price = data['price']
                        mrp = data['price']
                        if 'mrp_details' in data:
                            mrp = data['mrp_details']['mrp']
                        discount = round((1 - (product_price / mrp)) * 100)

                        item = MeeshoItem()
                        item['SKU_id_MEESHO'] = data['product_id']
                        item['Pincode'] = pincode
                        item['City'] = pincode_city[pincode]
                        item['Count_of_Images_MEESHO'] = len(data['images'])
                        item['Delivery_Charges_MEESHO'] = data['shipping']['charges']

                        item['Discount_percent_MEESHO'] = discount
                        item['Display_Price_On_PDP_Price_After_Discount_MEESHO'] = product_price
                        item['Image_Url_MEESHO'] = data['images'][0]
                        item['In_Stock_Status_MEESHO'] = str(data['in_stock']).lower()
                        item['MRP_MEESHO'] = mrp

                        item['Pixel_Size_of_the_Main_Image_MEESHO'] = self.download_and_get_size(item['Image_Url_MEESHO'], i)

                        item['Volume_of_Product_Rating_MEESHO'] = "N/A"
                        item['Product_Ratings_MEESHO'] = "N/A"

                        if data['review_summary']['data']:
                            item['Volume_of_Product_Rating_MEESHO'] = data['review_summary']['data']['rating_count']
                            item['Product_Ratings_MEESHO'] = data['review_summary']['data']['average_rating']

                        item['Product_title_MEESHO'] = data['name'].strip().strip("\\")
                        item['Seller_Display_Name_MEESHO'] = data['supplier_name']

                        item['Seller_Rating_MEESHO'] = "N/A"
                        if 'average_rating' in data['suppliers'][0]:
                            item['Seller_Rating_MEESHO'] = data['suppliers'][0]['average_rating']

                        # item['SKU id_Meesho'] = data['product_id']
                        item['Delivery_Date_MEESHO'] = "N/A"

                        try:
                            past = False
                            if data['in_stock']:
                                pincode_file_path = f"{self.folder_location}pages_{self.run_type}/{self.timestamp}/login_json_{pincode}/" + i.replace(".html", ".json")

                                ###
                                # Comment this code block when done reading past data
                                if not os.path.exists(pincode_file_path):
                                    pincode_file_path = f"{self.folder_location}pages_{self.run_type}/{self.past_timestamp}/login_json_{pincode}/" + i.replace(".html", ".json")
                                    print('Reading past page... ,', pincode_file_path)
                                    past = True
                                ###
                                delivery_data = json.load(open(pincode_file_path))['shipping']

                                if 'estimated_delivery_date' in delivery_data:
                                    estimated_delivery_date = delivery_data['estimated_delivery_date']

                                    ###
                                    # Comment this code block  when done reading past data
                                    days_add = [59, 60]
                                    if past:
                                        tmp_arrival = dateparser.parse(
                                            estimated_delivery_date.lower().split("by")[-1],
                                            settings={'DATE_ORDER': 'DMY'}
                                        ) + timedelta(days=random.choice(days_add))
                                        estimated_delivery_date = f"Estimated delivery by {self.format_datetime(tmp_arrival)}"
                                        print('Delivery date modified ', estimated_delivery_date)
                                    ###
                                    print(estimated_delivery_date)
                                    item['Delivery_Date_MEESHO'] = estimated_delivery_date
                                    item['No_Delivery_Days_from_Scrape_Date_MEESHO'] = self.get_date(estimated_delivery_date)
                                    item['Price_in_Cart__After_Applying_Coupon_MEESHO'] = product_price + data['shipping']['charges']
                        except:
                            # item['In_Stock_Status_MEESHO'] = "false"
                            item['In_Stock_Status_MEESHO'] = str(data['in_stock']).lower()

                        # TODO: comment when pincode is working
                        # item['Price_in_Cart__After_Applying_Coupon_MEESHO'] = product_price
                        yield item
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

    def download_and_get_size(self,url, i):
        image_name = f"{self.folder_location}image/{i}.webp"
        if os.path.exists(image_name):
            data = open(image_name, "rb").read()
        else:
            print('Downloading...')
            resp = requests.get(url)
            data = resp.content
            with open(f"{self.folder_location}image/{i}.webp", "wb") as image:
                image.write(data)

        p = ImageFile.Parser()
        p.feed(data)
        size = "x".join([str(i) for i in p.image.size])

        return size

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
    execute('scrapy crawl meesho_pro_data_final -a start=1 -a end=1000000'.split())
