import json
import os
import random
from datetime import datetime, timedelta
import dateparser
import pymysql
import requests
from PIL import ImageFile


timestamp = datetime.now().strftime("%Y%m%d")
# timestamp = '20241027'
past_timestamp = "20240909"

print('Reading...', timestamp)
# database = f"fk_meesho_vertial_master"
database = f"fk_meesho_master_mapping"
# database = f"fk_meesho_mapping"
# database = f"fk_meesho_searching"
# database = 'fk_meesho_image_mapping'
# database = 'fk_meesho_new_vertical'
# database = 'sy_meesho'
# database = 'snapdeal_meesho_vertical_mapping'

root_path = ""
if database == "sy_meesho":
    root_path = "D:/sy_Meesho/"

run_type = "master" if "master" in database else "normal"

con = pymysql.connect(host="172.27.131.60", user="root", password="actowiz", database=database)
crsr = con.cursor()


def get_day_suffix(day):
    if 4 <= day <= 20 or 24 <= day <= 30:
        return "th"
    else:
        return ["st", "nd", "rd"][day % 10 - 1]


def format_datetime(dt):
    day = dt.day
    suffix = get_day_suffix(day)
    formatted_date = dt.strftime(f"%A, {day}{suffix} %b")
    return formatted_date


def download_and_get_size(url, i):
    image_name = f"{root_path}image/{i}.webp"
    if os.path.exists(image_name):
        data = open(image_name, "rb").read()
    else:
        print('Downloading...')
        resp = requests.get(url)
        data = resp.content
        open(f"{root_path}image/{i}.webp", "wb").write(data)

    p = ImageFile.Parser()
    p.feed(data)
    size = "x".join([str(i) for i in p.image.size])

    return size


def get_date(string_obj, difference=0):
    arrival = dateparser.parse(string_obj.lower().split("by")[-1], settings={'DATE_ORDER': 'DMY'})

    return (arrival - datetime.now()).days
    # return (arrival - (datetime.now() + timedelta(days=1))).days


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
    files_list = os.listdir(f"{root_path}pages_{run_type}/{timestamp}/new_task_html")
    # timestamp = "20240622"
    for i in files_list:
        # if not (i.startswith('4xk7rq') or i.startswith("1942nn")):
        # if not i.startswith('yvf4a'):
        #     continue
        # print(i)

        input_product_id = i.split("_")[0]

        # if input_product_id not in ["1anlnp0",]:
        #     continue

        page = open(f"{root_path}pages_{run_type}/{timestamp}/new_task_html/" + i, "rb").read()
        try:
            data = page.split(b'id="__NEXT_DATA__" type="application/json">')[1].split(b"</script>")[0]
            data = json.loads(data)['props']['pageProps']['initialState']['product']['details']['data']
            if not data:
                continue
            product_price = data['price']
            mrp = data['price']
            if 'mrp_details' in data:
                mrp = data['mrp_details']['mrp']
            discount = round((1 - (product_price / mrp)) * 100)

            item = dict()
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

            item['Pixel_Size_of_the_Main_Image_MEESHO'] = download_and_get_size(item['Image_Url_MEESHO'], i)

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
                    pincode_file_path = f"{root_path}pages_{run_type}/{timestamp}/login_json_{pincode}/" + i.replace(".html", ".json")

                    ###
                    # Comment this code block when done reading past data
                    if not os.path.exists(pincode_file_path):
                        pincode_file_path = f"{root_path}pages_{run_type}/{past_timestamp}/login_json_{pincode}/" + i.replace(".html", ".json")
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
                                estimated_delivery_date.lower().split("by")[-1], settings={'DATE_ORDER': 'DMY'}
                            ) + timedelta(days=random.choice(days_add))
                            estimated_delivery_date = f"Estimated delivery by {format_datetime(tmp_arrival)}"
                            print('Delivery date modified ', estimated_delivery_date)
                        ###
                        print(estimated_delivery_date)
                        item['Delivery_Date_MEESHO'] = estimated_delivery_date
                        item['No_Delivery_Days_from_Scrape_Date_MEESHO'] = get_date(estimated_delivery_date)
                        item['Price_in_Cart__After_Applying_Coupon_MEESHO'] = product_price + data['shipping']['charges']
            except:
                # item['In_Stock_Status_MEESHO'] = "false"
                item['In_Stock_Status_MEESHO'] = str(data['in_stock']).lower()

            # TODO: comment when pincode is working
            # item['Price_in_Cart__After_Applying_Coupon_MEESHO'] = product_price

            print(input_product_id, data['product_id'])
            rows = ", ".join(list(item.keys()))

            updates = list()
            for i in item:
                if i == "Product_title_MEESHO" or i == "Seller_Display_Name_MEESHO":
                    item[i] = item[i].replace('"', "")
                updates.append(f'`{i}`="{item[i]}"')

            query = (f"update template_{timestamp} set {', '.join(updates)} where `SKU_id_MEESHO` = '{data['product_id']}' and `Pincode` = '{pincode}';")
            count = crsr.execute(query)
            # con.commit()
            print(count)
            if count == 0:
                query = (f"update template_{timestamp} set {', '.join(updates)} where `SKU_id_MEESHO` = '{input_product_id}' and `Pincode` = '{pincode}';")
                count = crsr.execute(query)
                # con.commit()
                print(count)

            # TODO
            # item['No Delivery Days from Scrape Date_Meesho'] = mrp
            final_data.append(item)
        except Exception as e:
            print(e)
            print(i)
            print(query)
            print("json_error", data)
            pass
    # input()
con.commit()
