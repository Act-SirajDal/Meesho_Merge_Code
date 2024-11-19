import gzip
import json
import pymysql
import os

# Database configuration
db_config = {
    'host': 'localhost',  # Replace with your MySQL host
    'user': 'root',  # Replace with your MySQL username
    'password': 'actowiz',  # Replace with your MySQL password
    'database': 'meesho_master'  # Replace with your MySQL database name
}
table_name = "meesho_pdp_data_20241119"  # Replace with the name of your existing table

# Directory containing .gz files
# gz_file_path = r'C:\Meesho\pages_master\20241119\new_task_html'
gz_file_path = r'D:\Meesho\pages_master\20241119\new_task_html'


# Step 1: Extract and read the .gz file
def read_gz_file(file_path):
    try:
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


# Step 2: Update data in MySQL table where sku_id matches
def update_supplier_id(sku_id, supplier_id, db_config, table_name):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    try:
        # Update the supplier ID where sku_id matches
        query = f"""
        UPDATE {table_name}
        SET Supplier_id_MEESHO = %s
        WHERE SKU_id_MEESHO = %s
        """
        cursor.execute(query, (supplier_id, sku_id))
        conn.commit()
        print(f"Successfully updated Supplier_id_MEESHO for SKU_id_MEESHO: {sku_id}.")
    except pymysql.Error as e:
        print(f"Error updating supplier_id for SKU_id {sku_id}: {e}")
    finally:
        conn.close()


# Step 3: Process all .gz files in the directory
def process_gz_files_in_directory(directory, db_config, table_name):
    files_processed = 0
    for file_name in os.listdir(directory):
        if file_name.endswith('.gz'):
            file_path = os.path.join(directory, file_name)
            print(f"Processing file: {file_path}")

            # Extract SKU ID from file name
            sku_id = file_name.split('_')[0]
            supplier_id = file_name.split('_')[1]

            if supplier_id:
                try:
                    supplier_id = str(supplier_id)
                    # Update the supplier_id in the database where sku_id matches
                    update_supplier_id(sku_id, supplier_id, db_config, table_name)
                    files_processed += 1
                except Exception as e:
                    print(f"Error processing file {file_name}: {e}")
    print(f"Finished processing {files_processed} files.")


# Main script
if __name__ == "__main__":
    process_gz_files_in_directory(gz_file_path, db_config, table_name)
