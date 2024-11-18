import sys
import gzip
import time
import db_config as db
import pymysql
from patchright.sync_api import sync_playwright

def check_delivery(page, i, pincode, local_cursor, local_connect):
    url = "https://www.meesho.com/s/p/" + i
    try:
        page.goto(url)
        pincode_input = page.locator('//input[@id="pin"]')
        pincode_input.wait_for(timeout=1000)
        pincode_input.fill(pincode)
        page.click('//button//span[contains(text(), "CHECK")]')

        delivery_text = page.locator("//span[contains(text(), 'Delivery by')]").text_content(timeout=2000)
        print(f"Delivery text: {delivery_text}", url)

        page_id = i + f'_{pincode}'
        with gzip.open(rf'C:\Meesho\pages_pincode\20241118\{page_id}.html.gz', 'wb') as save:
            save.write(bytes(page.content().encode()))
        update_query = f"update {db.db_links_table} set `status_{pincode}` = 'Done' where `meesho_pid` = '{i}'"
        local_cursor.execute(update_query)
        local_connect.commit()

    except Exception as e:
        print(f"URL: {url}, Error: {e}")
        error_message = str(e)
        if 'Delivery by' in error_message:
            update_query = f"update {db.db_links_table} set `status_{pincode}` = 'Not Found' where `meesho_pid` = '{i}'"
            local_cursor.execute(update_query)
            local_connect.commit()


def main(pstart, pend,pincode):
    print("Main function calling....")
    local_connect = pymysql.connect(
        host='localhost',
        user='root',
        password='actowiz',
        database=db.db_name
    )
    local_cursor = local_connect.cursor()

    start = time.time()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=r'C:\Siraj\Work\Meesho_Merge_Code\meesho\meesho\6359015644.json')

        def block_assets(route, request):
            if request.resource_type in ["stylesheet", "font", "image"] or request.url.endswith(".css") or request.url.endswith(".webp") or request.url.endswith(".woff2"):
                route.abort()
            else:
                route.continue_()

        page = context.new_page()
        page.route("**/*", block_assets)


        query = f"select `meesho_pid` FROM {db.db_links_table} where status='Done' and id between {pstart} and {pend} and status_{pincode}='pending'"
        print(query)
        local_cursor.execute(query)
        meesho_pids = local_cursor.fetchall()

        if not meesho_pids:
            print(f"No pending records for range {pstart} to {pend}. Skipping.")
            return

        for i in meesho_pids:
            check_delivery(page, i[0], pincode, local_cursor, local_connect)

        browser.close()

    time_taken = time.time() - start
    print(f"Time taken: {time_taken} seconds")


# Entry point of the script
if __name__ == '__main__':
    # Get `pstart` and `pend` from command-line arguments
    pstart = int(sys.argv[1])
    pend = int(sys.argv[2])
    pincode = str(sys.argv[3])
    print(pstart,pend,pincode)
    main(pstart, pend, pincode)
