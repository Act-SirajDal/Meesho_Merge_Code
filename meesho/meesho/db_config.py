from datetime import datetime

# DATABASE DETAILS
db_host = 'localhost'
db_user = 'root'
db_password = 'actowiz'

# db_name = 'fk_meesho_vertial_master'
# db_name = 'fk_meesho_new_vertical'
# db_name = 'fk_meesho_image_mapping'
# db_name = 'fk_meesho_searching'
db_name = 'meesho_master'
# db_name = 'fk_meesho_mapping'
# db_name = 'sy_meesho'
# db_name = 'snapdeal_meesho_vertical_mapping'

current_week = str(datetime.now().strftime("%Y%m%d"))
# current_week = '20240901'
db_links_table = ''
db_data_table = f'meesho__product_data_{current_week}'

template_table = f"template_{current_week}"