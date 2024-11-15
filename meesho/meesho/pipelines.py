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
        create_table_pdp = f'''
            CREATE TABLE IF NOT EXISTS `meesho_pdp_data_{DATE}` (
                `id` INT NOT NULL AUTO_INCREMENT,
                `SKU_id_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Count_of_Images_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Delivery_Charges_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Discount_percent_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Display_Price_On_PDP_Price_After_Discount_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Image_Url_MEESHO` VARCHAR(255) DEFAULT NULL,
                `In_Stock_Status_MEESHO` VARCHAR(255) DEFAULT NULL,
                `MRP_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Pixel_Size_of_the_Main_Image_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Volume_of_Product_Rating_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Product_Ratings_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Product_title_MEESHO` text DEFAULT NULL,
                `Seller_Display_Name_MEESHO` text DEFAULT NULL,
                `Seller_Rating_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Delivery_Date_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Pincode` VARCHAR(255) DEFAULT NULL,
                `City` VARCHAR(255) DEFAULT NULL,
                `No_Delivery_Days_from_Scrape_Date_MEESHO` VARCHAR(255) DEFAULT NULL,
                `Price_in_Cart__After_Applying_Coupon_MEESHO` VARCHAR(255) DEFAULT NULL,
                PRIMARY KEY (`id`)
            );
        '''

        spider.cursor.execute(create_table_pdp)
        spider.con.commit()

        create_table_pc = f'''
                    CREATE TABLE IF NOT EXISTS `meesho_pc_data_{DATE}` (
                        `id` INT NOT NULL AUTO_INCREMENT,
                        `SKU_id_MEESHO` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                        `Pincode` VARCHAR(255) DEFAULT NULL,
                        `City` VARCHAR(255) DEFAULT NULL,
                        `Delivery_Date_MEESHO` VARCHAR(255) DEFAULT NULL,
                        `No_Delivery_Days_from_Scrape_Date_MEESHO` VARCHAR(255) DEFAULT NULL,
                        PRIMARY KEY (`id`)
                    );
                '''

        spider.cursor.execute(create_table_pc)
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
                    values_data = item.values()
                    row_dict = dict(zip(item.keys(), values_data))
                    print(row_dict)
                    sku_id = row_dict.get('SKU_id_MEESHO')
                    spider.cursor.execute(insert_db, tuple(item.values()))
                    spider.logger.info(f'Data Inserted...')
                    update_query = f"update {db.db_links_table} set `status` = 'Done' where `meesho_pid` = '{sku_id}'"
                    spider.cursor.execute(update_query)
                    spider.con.commit()
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)

        if isinstance(item, MeeshoItemPCdata):
            try:
                # Id = item.pop('Id')
                field_list = []
                value_list = []
                for field in item:
                    field_list.append(str(field))
                    value_list.append('%s')
                fields = ','.join(field_list)
                values = ", ".join(value_list)
                insert_db = f"insert into {db.db_pin_data_table}( " + fields + " ) values ( " + values + " )"

                try:
                    # status = "Done"
                    values_data = item.values()
                    row_dict = dict(zip(item.keys(), values_data))
                    print(row_dict)
                    sku_id = row_dict.get('SKU_id_MEESHO')
                    spider.cursor.execute(insert_db, tuple(item.values()))
                    spider.con.commit()
                    spider.logger.info(f'Data Inserted...')
                    update_query = f"update {db.db_links_table} set `status_{spider.pincode}` = 'Done' where `meesho_pid` = '{sku_id}'"
                    spider.cursor.execute(update_query)
                    spider.con.commit()
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)
        return item
