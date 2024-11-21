import gzip
import json
import os
import random
import time
from datetime import datetime
import db_config as db
import pymysql
import dateparser
import requests
import sys
from evpn import ExpressVpnApi

def VPN_Change():
    api = ExpressVpnApi()# Connecting to VPN (BRAZIL)
    location_dict = open('meesho_valid_vpns.json','r',encoding='utf-8').read()
    loaction_loads = json.loads(location_dict)
    api.connect(country_id=random.choice(loaction_loads)['id'])  # BRAZIL country code for vpn
    time.sleep(5)  # keep some time delay before starting scraping because connecting
    print(api.locations)
    print('VPN Connected!' if api.is_connected else 'VPN Not Connected!')

local_connect = pymysql.connect(
        host='localhost',
        user='root',
        password='actowiz',
        database=db.db_name
    )
local_cursor = local_connect.cursor()
current_week = str(datetime.now().strftime("%Y%m%d"))
folder_path = rf'C:\Meesho\pages_master\{current_week}\new_task_html'
proxy = {
    'http':'http://9dbe950ef6284a5da9e7749db9f7cbd1:@api.zyte.com:8011/',
    'https': 'http://9dbe950ef6284a5da9e7749db9f7cbd1:@api.zyte.com:8011/'
}
start = 1
end = 50000

def get_date(string_obj, difference=0):
    arrival = dateparser.parse(string_obj.lower().split("by")[-1], settings={'DATE_ORDER': 'DMY'})
    return (arrival - datetime.now()).days

def main(pstart, pend):
    print("Main function calling....")
    select_query = f'''SELECT `SKU_id_MEESHO`,`Supplier_id_MEESHO`,`Image_Url_MEESHO` from {db.db_data_table} where `In_Stock_Status_MEESHO`="true" AND `pin_pagesave_status` = "pending" AND id BETWEEN {pstart} AND {pend}'''
    local_cursor.execute(select_query)
    meesho_pids = local_cursor.fetchall()
    for x in meesho_pids:
        # print(x)
        sku_id = x[0]
        supplier_id = x[1]
        image_url = x[2]
        file_path = folder_path+f'\\{sku_id}_{supplier_id}.html.gz'
        pincode_city = {
            "560001": "BANGALORE",
            # "110001": "DELHI",
            # "400001": "MUMBAI",
            # "700020": "KOLKATA",
        }

        # try:
        #     with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        #         response = f.read()
        # except Exception as e:
        #     print(f"Error reading file {file_path}: {e}")
        # data = response.split('id="__NEXT_DATA__" type="application/json">')[1].split("</script>")[0]
        # data = json.loads(data)['props']['pageProps']['initialState']['product']['details']['data']
        user_agent = ['Cronet','okhttp/4.9.0']
        print(random.choice(user_agent))
        if image_url:
            product_id = image_url.split('/')[-2]
            for pin in pincode_city.items():
                pincode = pin[0]
                city = pin[1]
                param = {
                    'dest_pin' : pincode,
                    'product_id' : product_id,
                    'supplier_id' : supplier_id,
                }
                # print(param)
                url = f'http://prod.meeshoapi.com/api/1.0/anonymous/shipping'
                # url = f'https://prod.meeshoapi.com/api/1.0/anonymous/shipping?dest_pin=560001&product_id=294205887&quantity=1&supplier_id=1057963'

                headers = {
                    'Accept-Encoding': 'gzip',
                    'APP-CLIENT-ID': 'android',
                    'APP-ISO-LANGUAGE-CODE': 'en',
                    'APP-SDK-VERSION': '28',
                    # 'App-Session-Id': '877dbf0c-bb00-4743-a465-e8e9d341aa63',
                    # 'APP-USER-LOCATION': 'eyJsYXQiOiIxOC45NDc0IiwibG9uZyI6IjcyLjgxMzgiLCJwaW5jb2RlIjoiNDAwMDAxIiwiY2l0eSI6Ik11bWJhaSIsImFkZHJlc3NfaWQiOm51bGx9',
                    'App-Version': '21.0',
                    'App-Version-Code': '632',
                    'Application-Id': 'com.meesho.supply',
                    'Authorization': '32c4d8137cn9eb493a1921f203173080',
                    'Connection': 'Keep-Alive',
                    'Country-Iso': 'in',
                    'Host': 'prod.meeshoapi.com',
                    'Instance-Id': '3225712037ce488294a2460b24ef7cd3',
                    'MEESHO-USER-CONTEXT': 'anonymous',
                    'SHIELD-SESSION-ID': '',
                    'User-Agent': random.choice(user_agent),
                    'Xo': 'eyJ0eXBlIjoiY29tcG9zaXRlIn0=.eyJqd3QiOiJleUpvZEhSd2N6b3ZMMjFsWlhOb2J5NWpiMjB2ZG1WeWMybHZiaUk2SWpFaUxDSm9kSFJ3Y3pvdkwyMWxaWE5vYnk1amIyMHZhWE52WDJOdmRXNTBjbmxmWTI5a1pTSTZJa2xPSWl3aVlXeG5Jam9pU0ZNeU5UWWlmUS5leUpwWVhRaU9qRTNNekU1T1RNME9Ua3NJbVY0Y0NJNk1UZzRPVFkzTXpRNU9Td2lhSFIwY0hNNkx5OXRaV1Z6YUc4dVkyOXRMMmx1YzNSaGJtTmxYMmxrSWpvaU16SXlOVGN4TWpBek4yTmxORGc0TWprMFlUSTBOakJpTWpSbFpqZGpaRE1pTENKb2RIUndjem92TDIxbFpYTm9ieTVqYjIwdllXNXZibmx0YjNWelgzVnpaWEpmYVdRaU9pSTJaRFE0T0RRNU15MWlZelkxTFRRNFltVXRPRFJqTVMwd1ltSTFZalF6T1RCa01EVWlmUS42TUJOSnhkbFVHWmEtR21xcDFjWWZ3YkNMVDNnVlF4dnhuMWdUQ2lKN0lBIiwieG8iOm51bGx9',
                }
                time.sleep(1)
                # req = requests.get(url=url,params=param, headers=headers,proxies=proxy,verify=False)
                req = requests.get(url=url,params=param, headers=headers)
                print(req.text)
                print(req.status_code)
                if req.status_code != 200:
                    req = requests.get(url=url,params=param, headers=headers,proxies=proxy,verify=False)
                    if req.status_code != 200:
                        # VPN_Change()
                        req = requests.get(url=url, params=param, headers=headers, proxies=proxy, verify=False)
                page_id = str(sku_id) + f'_{pincode}'
                if 'estimate' in req.text:
                    file_dir = rf'C:\Meesho\pages_master\{current_week}\login_json_{pincode}'
                    if not os.path.exists(file_dir):
                        os.makedirs(file_dir)
                    with gzip.open(rf'{file_dir}\{page_id}.html.gz', 'w') as save:
                        save.write(req.content)
                    json_load = json.loads(req.content)
                    Delivery_Date_MEESHO = json_load['shipping']['estimated_delivery_date']
                    No_Delivery_Days_from_Scrape_Date_MEESHO = get_date(Delivery_Date_MEESHO)
                    try:
                        query = f"""
                            INSERT INTO {db.db_pin_data_table} (
                                SKU_id_MEESHO, 
                                Pincode, 
                                City, 
                                Delivery_Date_MEESHO, 
                                No_Delivery_Days_from_Scrape_Date_MEESHO
                            ) VALUES (%s, %s, %s, %s, %s);
                            """
                        local_cursor.execute(query, (sku_id, pincode, city, Delivery_Date_MEESHO, No_Delivery_Days_from_Scrape_Date_MEESHO))
                        local_connect.commit()
                        print("Record successfully inserted.")
                        update_query = f"update {db.db_data_table} set `pin_pagesave_status` = 'Done' where `SKU_id_MEESHO` = '{sku_id}'"
                        local_cursor.execute(update_query)
                        local_connect.commit()
                    except pymysql.Error as e:
                        print(f"Error inserting record: {e}")
                elif req.status_code != 200:
                    pass


# Entry point of the script
if __name__ == '__main__':
    # Get `pstart` and `pend` from command-line arguments
    # pstart = int(sys.argv[1])
    # pend = int(sys.argv[2])
    pstart = 1
    pend = 50000
    print(pstart,pend)
    main(pstart, pend)