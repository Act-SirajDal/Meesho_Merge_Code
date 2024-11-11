import sys

start_part = 000000
try:
    end_part = int(sys.argv[1])
except:
    end_part = 172979

all_parts = list()
all_parts.append('taskkill /F /FI "WindowTitle eq meesho_product_*"')

vertical = True if len(sys.argv) > 2 else False

parts = 30
step = (end_part - start_part) // parts
zfill_step = len(str(end_part))

for i in range(start_part, end_part, step):
    start = str(i + 1).zfill(zfill_step)
    end = str(i + step).zfill(zfill_step)
    part = f'start "meesho_product_{start}_{end}" scrapy crawl products -a start={start} -a end={end}'
    all_parts.append(part)

open("D:/deep/meesho/meesho/spiders/runthis.bat", "w").write("\n".join(all_parts))