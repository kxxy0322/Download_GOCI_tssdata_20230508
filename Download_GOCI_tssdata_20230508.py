import requests
import os
import random
import time
from datetime import datetime, timedelta

base_url = 'http://kosc.kiost.ac.kr//download/downService.do?fileName=/home/goci/nfsdb/COMS/GOCI/L2'

start_date = datetime(2020, 1, 1)  # 开始日期
end_date = datetime(2020, 12, 31)  # 结束日期

path = 'D:/GOCI/DATA/TSS'
os.makedirs(path, exist_ok=True)

file_name = 'COMS_GOCI_L2A_GA_{}.TSS.he5.zip'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

current_date = start_date
while current_date < end_date:
    current_path = os.path.join(path, str(current_date.year),
                                f'TSS_{current_date.year}_{current_date.month}')
    os.makedirs(current_path, exist_ok=True)

    for j in range(8):
        for k in range(35, 46):
            date_str_no_dash = current_date.strftime('%Y%m%d') + f'{j:02d}16{k:02d}'
            url = base_url + f'/{current_date.strftime("%Y/%m/%d")}/L2/{file_name.format(date_str_no_dash)}'
            file_path = os.path.join(current_path, file_name.format(date_str_no_dash))

            # 设置请求间隔
            time.sleep(random.uniform(0.5, 1))
            try:
                with requests.get(url, headers=headers, stream=True, timeout=10) as r:
                    r.raise_for_status()
                    if int(r.headers['Content-Length']) >= 1024:
                        start_time = time.time()
                        with open(file_path, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                                    elapsed_time = time.time() - start_time
                                    if elapsed_time > 120:  # 超过两分钟未下载完该链接内的文件，则跳过该链接的下载
                                        print(f'Timeout, skip file {file_path}.')
                                        break
                        if elapsed_time <= 120:  # 如果文件下载时间不足两分钟，则输出下载完成信息
                            print(f'Download completed: {file_path}')

            except requests.exceptions.RequestException as e:
                print(f'Failed to download {url}: {e}')

    current_date += timedelta(days=1)
