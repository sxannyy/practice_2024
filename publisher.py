import asyncio
from gnss_tec import rnx
from download_info import download_info, decompress_all_data
from datetime import date, timedelta
import time

start_time = time.time()
asyncio.run(download_info(date(2024,1,1)))
# asyncio.run(download_info(date.today() - timedelta(days=5)))
asyncio.run(decompress_all_data())

end_time = time.time()
print(start_time - end_time)

with open('./data/DAEJ00KOR_R_20240010000_01D_30S_MO.rnx') as obs_file:
    reader = rnx(obs_file)
    prev_epoch = None
    for tec in reader:
        if prev_epoch is None:
            prev_epoch = tec.timestamp
        if tec.timestamp != prev_epoch:
            time.sleep(30)
            prev_epoch = tec.timestamp
        print(
            '{} {}: {} {}'.format(
                tec.timestamp,
                tec.satellite,
                tec.phase_tec,
                tec.p_range_tec,
            )
        )
