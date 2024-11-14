import pandas as pd
import pymysql

# Establish a connection to your MySQL database
conn = pymysql.connect(
    host="172.27.131.60",
    user="root",
    password="actowiz",
    database="sd_meesho_master"
)

# Load data from MySQL tables into DataFrames
product_data_df = pd.read_sql("SELECT * FROM meesho_pdp_data_20241113", conn)
delivery_data_df = pd.read_sql("SELECT * FROM meesho_pc_data_20241113", conn)

print(delivery_data_df.columns)

# Close the connection if it's no longer needed
conn.close()

# Merge product data with delivery data on SKU_ID and Pincode
merged_df = product_data_df.merge(
    delivery_data_df,
    on=['SKU_id_MEESHO', 'Pincode'],
    how='left'  # Use 'left' join to keep all records in the product data table
)
print(merged_df.columns)
# Now merged_df contains both product and delivery data; you can update the product data as needed
# For example, if you need to map a specific column, let's say `delivery_status`, from the delivery table to the product table:
product_data_df['Delivery_Date_MEESHO'] = merged_df['Delivery_Date_MEESHO_x']  # Map the column
product_data_df['No_Delivery_Days_from_Scrape_Date_MEESHO'] = merged_df['No_Delivery_Days_from_Scrape_Date_MEESHO_x']  # Map the column
product_data_df['Price_in_Cart__After_Applying_Coupon_MEESHO'] = merged_df['Delivery_Charges_MEESHO'].astype(float) + merged_df['Display_Price_On_PDP_Price_After_Discount_MEESHO'].astype(float)  # Map the column

print(product_data_df.columns)
