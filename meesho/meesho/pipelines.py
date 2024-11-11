# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymysql import IntegrityError
from meesho.items import *
import meesho.db_config as db
from datetime import datetime

DATE = str(datetime.now().strftime("%Y%m%d"))

class MeeshoPipeline:
    def process_item(self, item, spider):
        create_table = f'''
            CREATE TABLE IF NOT EXISTS `meesho__product_data_{DATE}` (
                `id` INT NOT NULL AUTO_INCREMENT,
                `SKU_id_MEESHO` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                `Count_of_Images_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Delivery_Charges_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Discount_percent_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Display_Price_On_PDP_Price_After_Discount_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Image_Url_MEESHO` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                `In_Stock_Status_MEESHO` VARCHAR(255) DEFAULT NULL,
                `MRP_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Pixel_Size_of_the_Main_Image_MEESHO` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                `Volume_of_Product_Rating_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Product_Ratings_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Product_title_MEESHO` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                `Seller_Display_Name_MEESHO` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                `Seller_Rating_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Delivery_Date_MEESHO` VARCHAR(255) DEFAULT NULL,
                PRIMARY KEY (`id`)
            );
        '''

        spider.cursor.execute(create_table)
        spider.con.commit()

        if isinstance(item, MeeshoItem):
            try:
                # Id = item.pop('Id')
                field_list = []
                value_list = []
                for field in item:
                    field_list.append(str(field))
                    value_list.append('%s')
                fields = ','.join(field_list)
                values = ", ".join(value_list)
                insert_db = f"insert into {db.db_data_table}( " + fields + " ) values ( " + values + " )"

                try:
                    # status = "Done"
                    spider.cursor.execute(insert_db, tuple(item.values()))
                    spider.con.commit()
                    spider.logger.info(f'Data Inserted...')
                except IntegrityError as e:
                    print("IntegrityError....",e)
            except Exception as e:
                print(e)
