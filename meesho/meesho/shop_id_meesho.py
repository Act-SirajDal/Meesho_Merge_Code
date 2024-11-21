import json
import os
import gzip
import pandas as pd

gz_file_path = r'C:\Meesho\pages_master\20241120\new_task_html'


# Step 1: Extract and read the .gz file
def read_gz_file(file_path):
    try:
        with gzip.open(rf'{file_path}', 'rt', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

# Initialize a list to store the extracted data
data_list = []

count = 0
for i in os.listdir(gz_file_path):
    file_path = gz_file_path+ '\\'+ i
    print(file_path)
    response = read_gz_file(file_path)

    pro_data = response.split('id="__NEXT_DATA__" type="application/json">')[1].split("</script>")[0]
    data = json.loads(pro_data)['props']['pageProps']['initialState']['product']['details']['data']
    print(data)
    print(data['suppliers'][0]['handle'])

    meesho_pid = i.split('_')[0]
    supplier_handle_id = data['suppliers'][0]['handle']
    if supplier_handle_id:
        supplier_handle_url = f'https://www.meesho.com/{supplier_handle_id}?ms=2'
    else:
        supplier_handle_url = "NA"
    count = count + 1
    # Append the row data as a dictionary
    data_list.append({
        "ID": count,
        "Meesho PID": meesho_pid,
        "Supplier Handle ID": supplier_handle_id,
        "Supplier Handle URL": supplier_handle_url
    })
    # break

# Create a DataFrame from the data
df = pd.DataFrame(data_list)

# Save the DataFrame to an Excel file
output_file = "meesho_data.xlsx"  # Specify your desired file name
df.to_excel(output_file, index=False)
print(f"Excel file saved as {output_file}")