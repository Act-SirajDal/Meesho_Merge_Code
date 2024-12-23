import requests
import json
import os
import random
import time
from datetime import datetime, timedelta
from typing import Iterable
from meesho.items import *
import pymysql
import scrapy
from scrapy import Request, Spider
from scrapy.cmdline import execute
import meesho.db_config as db
from PIL import ImageFile
import gzip


class MeeshoFSpider(scrapy.Spider):
    name = "meesho_pro_data_final"
    allowed_domains = ["meesho.com"]
    start_urls = ["https://meesho.com"]
    handle_httpstatus_list = [403, 429, 400]
    folder_location = f"C:/Meesho/"
    errors = list()

    DATE = '20241120'
    # DATE = str(datetime.now().strftime("%Y%m%d"))

    def __init__(self, name=None, start=0, end=100000, dbname=DATE, **kwargs):
        super().__init__(name, **kwargs)
        # DATABASE SPECIFIC VALUES
        self.start = start
        self.end = end
        db.db_links_table = f'product_links_{dbname}'
        self.timestamp = dbname
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

        # query = f"select `meesho_pid` FROM {db.db_links_table} where status='pending' and id between {self.start} and {self.end} limit 200;"
        query = f"select `meesho_pid` FROM {db.db_links_table} where status='pending' and id between {self.start} and {self.end};"
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

        i_o = kwargs['page_name']
        i = str(i_o).replace("\\","")

        status = "pending"
        data = response.body.split(b'id="__NEXT_DATA__" type="application/json">')[1].split(b"</script>")[0]
        data = json.loads(data)['props']['pageProps']['initialState']['product']['details']['data']
        if data:
            if data['valid']:
                if 'suppliers' not in data:
                    return None
                supplier = data['suppliers'][0]
                supplier_name = str(supplier['id'])

                page = ''
                file_path = self.folder_location + i + f"_{supplier_name}.html.gz"
                # Writing the Gzip file safely
                with gzip.open(file_path, "wb") as f:
                    f.write(response.body)
                with gzip.open(file_path, "rb") as f:
                    page = f.read().decode("utf-8")
                    print(type(page))
                data = page.split('id="__NEXT_DATA__" type="application/json">')[1].split("</script>")[0]
                data = json.loads(data)['props']['pageProps']['initialState']['product']['details']['data']
                if data:
                    status = "Done"
                    product_price = data['price']
                    mrp = data['price']
                    if 'mrp_details' in data:
                        mrp = data['mrp_details']['mrp']
                    discount = round((1 - (product_price / mrp)) * 100)

                    item = MeeshoItem()
                    item['SKU_id_MEESHO'] = data['product_id']
                    item['Supplier_id_MEESHO'] = supplier_name
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

                item['Delivery_Date_MEESHO'] = "N/A"
                item['Pincode'] = ''
                item['City'] = ''
                item['No_Delivery_Days_from_Scrape_Date_MEESHO'] = ''
                item['Price_in_Cart__After_Applying_Coupon_MEESHO'] = ''
                print(data['product_id'])
                yield item
            else:
                status = "This product is out of stock"
                update_query = f"update {db.db_links_table} set `status` = '{status}' where `meesho_pid` = '{i_o}'"
                self.cursor.execute(update_query)
                self.con.commit()
        else:
            status = "Not Found page"
            update_query = f"update {db.db_links_table} set `status` = '{status}' where `meesho_pid` = '{i_o}'"
            self.cursor.execute(update_query)
            self.con.commit()

        # TODO: DON'T UNCOMMENT THIS UNTIL GET CONFIRMATION FROM DEEP
        # if f'"in_stock":false,"product_id":"{i}"':
        #     status = "Out of Stock while add to cart"

    def download_and_get_size(self, url, i):
        image_name = f"{self.folder_location}image/{i}.webp"
        try:
            if os.path.exists(image_name):
                # Read the image data if it already exists
                data = open(image_name, "rb").read()
            else:
                print("Downloading...")
                # Download the image
                resp = requests.get(url)
                data = resp.content
                # Save the image
                with open(image_name, "wb") as image_file:
                    image_file.write(data)

            # Parse the image
            p = ImageFile.Parser()
            p.feed(data)
            image = p.close()
            size = "x".join([str(dim) for dim in image.size])
            print("Image size:", size)
            return size

        except Exception as e:
            print("Error parsing image:", e)
            # Remove the file if parsing fails
            if os.path.exists(image_name):
                try:
                    os.remove(image_name)
                    print(f"Deleted corrupted image: {image_name}")
                except Exception as delete_error:
                    print(f"Failed to delete image: {delete_error}")


if __name__ == '__main__':
    # execute('scrapy crawl meesho_pro_data_final -a start=1 -a end=10000000'.split())
    execute('scrapy crawl meesho_pro_data_final -a start=1 -a end=10'.split())
