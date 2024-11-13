import json
import os
import random
import time
from datetime import datetime
from typing import Iterable, Optional, Any, Union

import pymysql
import scrapy
from scrapy import Request, Spider
from scrapy.cmdline import execute
from twisted.internet.defer import Deferred

import meesho.db_config as db


class PincodeDetailsSpider(scrapy.Spider):
    name = "pincode_details"
    allowed_domains = ["meesho.com"]
    start_urls = ["https://meesho.com"]
    handle_httpstatus_list = [500, 520, 410, 400, 401, 521]
    oos_list = list()
    cookies_folder = "D:/Meesho/cookies"
    page_save_root = "D:/Meesho/"
    custom_settings = {
        "CONCURRENT_REQUESTS": 16,
        "REFERER_ENABLED": False,
    }

    def __init__(self, name: Optional[str] = None, pincode: str = "560001", dbname=str(datetime.now().strftime("%Y%m%d")), start=0, end=100000, **kwargs: Any):
    # def __init__(self, name: Optional[str] = None, pincode: str = "560001",dbname='20240918', start=0, end=100000, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.start = start
        self.end = end
        self.pincode = str(pincode).strip()
        self.timestamp = dbname
        self.run_type = "master" if "master" in db.db_name else "normal"

        if db.db_name == "sy_meesho":
            self.page_save_root = f"D:/sy_Meesho/"

        self.folder_location = f"{self.page_save_root}pages_{self.run_type}/{self.timestamp}/new_task_html/"
        self.pincode_folder_location = f"{self.page_save_root}pages_{self.run_type}/{self.timestamp}/login_json_{pincode}/"
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

        query = f"select `meesho_pid` FROM {db.db_links_table} where status='Done' and id between {self.start} and {self.end} and status_{self.pincode}='pending' limit {len(pincode_cookies)};"
        print(query)
        self.cursor.execute(query)
        query_results = self.cursor.fetchall()
        self.logger.info(f"\n\n\nTotal Results ...{len(query_results)}\n\n\n", )
        query_results = [k[0] for k in query_results]

        for i in os.listdir(self.folder_location):
            name_list = i.rsplit(".", 1)[0].split("_")
            if name_list[0] in query_results:
                post_json_data = {
                    'dest_pin': f'{self.pincode}',
                    'product_id': f'{name_list[0]}',
                    'supplier_id': int(name_list[1]),
                    'quantity': 1,
                }
                # url = f"https://www.meesho.com/api/v1/shipping"
                url = f"https://www.meesho.com/api/v1/check-shipping-delivery-date"

                headers = {
                    'accept': 'application/json, text/plain, */*',
                    'accept-language': 'en-GB,en;q=0.9',
                    'content-type': 'application/json',
                    'cookie': 'ANONYMOUS_USER_CONFIG=j%3A%7B%22clientId%22%3A%22b68345fd-e77d-4085-abe7-6fca2ac4%22%2C%22instanceId%22%3A%22b68345fd-e77d-4085-abe7-6fca2ac4%22%2C%22xo%22%3A%22eyJ0eXBlIjoiY29tcG9zaXRlIn0%3D.eyJqd3QiOiJleUpvZEhSd2N6b3ZMMjFsWlhOb2J5NWpiMjB2ZG1WeWMybHZiaUk2SWpFaUxDSm9kSFJ3Y3pvdkwyMWxaWE5vYnk1amIyMHZhWE52WDJOdmRXNTBjbmxmWTI5a1pTSTZJa2xPSWl3aVlXeG5Jam9pU0ZNeU5UWWlmUS5leUpwWVhRaU9qRTNNalkyTmpnMU5qRXNJbVY0Y0NJNk1UZzRORE0wT0RVMk1Td2lhSFIwY0hNNkx5OXRaV1Z6YUc4dVkyOXRMMmx1YzNSaGJtTmxYMmxrSWpvaVlqWTRNelExWm1RdFpUYzNaQzAwTURnMUxXRmlaVGN0Tm1aallUSmhZelFpTENKb2RIUndjem92TDIxbFpYTm9ieTVqYjIwdllXNXZibmx0YjNWelgzVnpaWEpmYVdRaU9pSmpNV0U0WW1VMk1pMW1aREE1TFRRd01tSXRPRGxpWkMwNE5UWTJOakpoWWpnNE1ERWlmUS5IdUN3cDNEbERGZjNiTlNhQnFVZHdBdXRkaHphb1huQ2Zic3htWENScVp3IiwieG8iOm51bGx9%22%2C%22createdAt%22%3A%222024-09-18T14%3A09%3A21.137Z%22%7D; CAT_NAV_V2_COOKIE=0.01229192451795158; ak_bmsc=087B1919D2ED03559492FA98C3FF8039~000000000000000000000000000000~YAAQrowsMdXzk9iRAQAAtc1fBhmitPMM4VdhLqywfwEnf5Yzrd1g5IsjzgL8u0WqmPXQftxvHyxPy1DVX2E6OcKLbMmAjmKuNaJlYE4f4qai32CgRMpAo5zJvDPThQpVUrXG/XPUWT4JoNTUU4lVy1Tjj9OnahSo3Dyk4BKVjZ4X6XweGgO4OKtu9WAIOxwjRuUob5gK/bgxpUx+qmS16dAmPteSsDfonCdPuqoVrQmv3062kheAv6BNRMvVtYzJHJdB6gyiuPNQ63yDJNp+D3R0pzL4vD/cuNaf9mddvmh/my1yd9r8F0T6SXXvbWVAqQtJYpCOYURJ0tOjhYrVUmiagP+1fw82tz4t//TsMK6TkXB76I69SqWIyiwAD3+D8YZiK0dyD/kkD4laP5K2STFXNgGG7fdGemMKl16yF5nEnjfmRAubEvCVw7Y6U8BPCq5MIA/hwn2TsZLg4U0bQgobfbdLDbFTCqnztzuC6w==; __logged_in_user_id_=125742181; _is_logged_in_=1; __connect.sid__=s%3AVszWhTLPr9564h0j5O_H_3ufmoaI_d3R.NjNcfHdck1mu3nINbGsqPJV%2B4BAJ8GgdQV86%2FD8SowU; bm_sz=8144B19A3F71BC1CF24CC7CAFD8AFFF9~YAAQ5owsMZHx38ORAQAAOe1gBhnHqaxDHV/tyhFOkbrJvoytbuR+xGidY5TLY9SNaEMWq745miT3GYvSc6XQWQg0GPIEC081ty+cy1wqeebZb/bBeM3JXUfxzM0nuFiy9L1wf6zhqv0Ub7gisbwAIczXR49PyQxKRlWgaoEnDnKmFaUubg4d7BN6EJkl4esn3Vh9ZGU2Y7+QqornIUc94shC49TJIZsinxzws86rUjueJpox9NGaEJoDREGOet8Juc9h0xMnqAlF2tXSQia5QhXTZzLzRiKtj7ob73/26yygIrEvGFsvpIFQVuiHqWvL2ibOqqkjygp8y4+9OiC+cWKPBDoGw3mbaJ1tnUt1Z21XNotpKbptUtrXU4Z2yitgKxIWy9aN4LjhDWG7bHimy5c1jA8ivq7lpqwRPJFS0sfL9TOFNGRxiAexj0gEz50du0aHGbwZScLERdR1MCiTmGOj1H2HgFgfF1S0~4339526~4343363; location-details=%7B%22city%22%3A%22Bengaluru%22%2C%22pincode%22%3A%22560001%22%2C%22lat%22%3A%2213.2257%22%2C%22long%22%3A%2277.575%22%7D; _abck=C195AACF087B5EB3FD1767ACDC2DACC2~-1~YAAQrowsMeMhlNiRAQAAsX9jBgz2pi3Mt3SwAF/essNYkt8ByL3t/OT5GKqlyYa8j3h2/QGitdS2yYCS0AlbKQubtpjrX9dyIfgUiB5G2GInRyKJWIdw/uQZQd+6yhjOPTXeBF12jOSw3xrin3WJKxCibPy5g53ESd3BD2KsfP/BwtYKR7apR42wlDCNQr68rzTh0xTj1oXzR/zSORye4NPo7o0mRln/hSiFF51KY1tBpvDkPoDAqmfCjs1M1XYWpjviDnv5/KbD69kGWcRx43oY3wZZ84i3I3W9apqLL60alMwJ04iJGWJyi62MUIoT2tzbw6SpytN2g9/8rJ1hPVtmXcUDOkmuUbFq+remm4BbZNDVvIJ1ZZodN9KfKAt1X5P+78SnFXgFIzYJlVdCjhbogTqwhk7T7yid9VMikkLXe3ePTFDnGc0F1wla2bRwgWav2aPkcChpChjngktFf0KdOMdyp4/+BBScNaUIV/pdTThd1lCGRXgW0G7YE2lGfN+uTfMg6SpY2dvrAlofy8BKs7EkWHIKy2kdGBP9RAaRyLkykHJgIsHQNdzAXGkOzoC4TGDzwDbrvtDkft0Myc6cG8g7B1YTV1eLj1nS+nW6rGXUY7L5iR1V8jZislJ4Rw==~-1~||0||~1726687394; INP_POW=0.9469540676280128; bm_sv=FFE8BC6006C566BB2EAE3B81604C73CA~YAAQrowsMRcilNiRAQAAgoJjBhnASvjuJo4YGe9u/MPO6nw+lNzPk7QpEeIUJhONMIAyQH3pPgUgVrRyih3pSWybUcyhYhLJWa+AXnzG5FrAOtRuQbeUTuSE8hoLKx+CYMg0b8MUQWoZ/5I98b9PnKRzNx/J/pB0qwH3wsynZ8dPJXG9GoHO06ryedUyeOFJdtL39DZAJQasOSa1uRde0tUoZHsSJCh6ho9asF5d7FGTwKeuy8UMexnE8SEzLAWEUw==~1; mp_60483c180bee99d71ee5c084d7bb9d20_mixpanel=%7B%22distinct_id%22%3A%20%22192065fdcf08a2-02d6673dee4645-26011851-144000-192065fdcf1870%22%2C%22%24device_id%22%3A%20%22192065fdcf08a2-02d6673dee4645-26011851-144000-192065fdcf1870%22%2C%22Session%20ID%22%3A%20%223d56cb5a-7344-481a-9ff0-a2e8ff73%22%2C%22last%20event%20time%22%3A%201726684044462%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22%24user_id%22%3A%20125742181%2C%22Is%20Anonymous%22%3A%20%22False%22%2C%22Instance_Id%22%3A%20%22b68345fd-e77d-4085-abe7-6fca2ac4%22%2C%22V2%20Cat-Nav%20Exp%20Enabled%22%3A%20true%2C%22__alias%22%3A%20125742181%7D',
                    'meesho-iso-country-code': 'IN',
                    'origin': 'https://www.meesho.com',
                    'priority': 'u=1, i',
                    'referer': 'https://www.meesho.com/black-jeans/p/7837id',
                    'sec-ch-ua': '"Chromium";v="131", "Not_A Brand";v="24"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
                }

                yield scrapy.Request(
                    method='POST',
                    url=url,
                    body=json.dumps(post_json_data),
                    headers=headers,
                    # cookies=pincode_cookies[count],
                    cb_kwargs={
                        "i": i,
                        "name_list": name_list,
                        "retry_410": 0,
                        "retry_401": 0,
                    },
                    # meta={"impersonate": random.choice(["chrome110", "edge99", "safari15_5"])},
                    dont_filter=True,
                    # headers={
                    #     'referer': 'https://www.meesho.com/s/p/' + name_list[0],
                    #     # 'MEESHO-ISO-COUNTRY-CODE': 'IN',
                    #     # 'Accept': 'application/json, text/plain, */*',
                    # }
                )
                count += 1

    def parse(self, response, **kwargs):
        print(response.text)
        name_list = kwargs['name_list']

        if response.status == 500:
            self.oos_list.append(kwargs['i'])
            self.logger.info(f"{kwargs['i']} out of stock")
        elif response.status in [401, 410]:
            yield self.retry_on_gt_400(response, name_list[0], **kwargs)
            return None
        elif response.status == 200:
            self.logger.info(f"{kwargs['i']} Found")
            open(f"{self.pincode_folder_location}/{name_list[0]}_{name_list[1]}.json", "wb").write(response.body)
            update_query = f"update {db.db_links_table} set `status_{self.pincode}` = 'Done' where `meesho_pid` = '{name_list[0]}'"
            self.cursor.execute(update_query)

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

if __name__ == '__main__':
    pass
    execute("scrapy crawl pincode_details -a pincode=560001 -a start=4430 -a end=4430".split())
    # for i in range(1, 180):
    #     print(i)
    #     os.system('taskkill /F /FI "WindowTitle eq meesho_pincode_*"')
    #
    #     os.system('start "meesho_pincode_110001" scrapy crawl pincode_details -a pincode=110001 -a start=1 -a end=23000 -a dbname=20240622')
    #     os.system('start "meesho_pincode_400001" scrapy crawl pincode_details -a pincode=400001 -a start=1 -a end=23000 -a dbname=20240622')
    #     os.system('start "meesho_pincode_560001" scrapy crawl pincode_details -a pincode=560001 -a start=1 -a end=23000 -a dbname=20240622')
    #     os.system('start "meesho_pincode_700020" scrapy crawl pincode_details -a pincode=700020 -a start=1 -a end=23000 -a dbname=20240622')
    #     os.system('start "meesho_pincode_110001" scrapy crawl pincode_details -a pincode=110001 -a end=46000 -a start=23001 -a dbname=20240622')
    #     os.system('start "meesho_pincode_400001" scrapy crawl pincode_details -a pincode=400001 -a end=46000 -a start=23001 -a dbname=20240622')
    #     os.system('start "meesho_pincode_560001" scrapy crawl pincode_details -a pincode=560001 -a end=46000 -a start=23001 -a dbname=20240622')
    #     os.system('start "meesho_pincode_700020" scrapy crawl pincode_details -a pincode=700020 -a end=46000 -a start=23001 -a dbname=20240622')
    #
    #     time.sleep(120)
