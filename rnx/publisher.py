from datetime import datetime
from hashlib import md5
from gnss_tec import rnx
import paho.mqtt.client as mqtt_client
import time
import os
import sys


broker="broker.emqx.io"

def process_file(folder_path, filename):
    with open(f'{folder_path}/{filename}.rnx') as obs_file:
        reader = rnx(obs_file)
        prev_epoch = None
        data = []
        prev_system_time = time.time()
        make_sleep = False
        time_flag = True
        for tec in reader:
            time_str = str(tec.timestamp)
            given_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").time()
            current_time = datetime.now().time()
            given_seconds = given_time.hour * 3600 + given_time.minute * 60 + given_time.second
            current_seconds = current_time.hour * 3600 + current_time.minute * 60 + current_time.second
            difference_in_seconds = current_seconds - given_seconds

            if difference_in_seconds > 30:
                continue
            while make_sleep and time.time() - prev_system_time <= 30:
                pass
            make_sleep = False
            if prev_epoch is None:
                prev_epoch = tec.timestamp
            if tec.timestamp != prev_epoch:
                print("Prepare for sleeping", prev_epoch, tec.timestamp, flush=True)
                yield data
                prev_system_time = time.time()
                make_sleep = True
                data = []
                prev_epoch = tec.timestamp
            data.append( 
                '{} {}: {} {}'.format(
                    tec.timestamp,
                    tec.satellite,
                    tec.phase_tec,
                    tec.p_range_tec,
                )
            )
        data.append( 
            'Данные кончились, следующая порция данных добавиться после некоторой задержки'
        )
        yield data


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: publisher.py <date> <filename>")
        sys.exit(1)
    
    date = sys.argv[1]
    folder_path = os.path.join("/home/ivan/praktika/data", date)
    filename = sys.argv[2]
    filename_path = folder_path + '/' + sys.argv[2] + '.rnx'
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist.")
        sys.exit(1)
    
    if not os.path.exists(filename_path):
        print(f"File {filename_path} does not exist.")
        sys.exit(2)

    client = mqtt_client.Client(
        mqtt_client.CallbackAPIVersion.VERSION1, 
        md5(str(datetime.now()).encode('utf-8')).hexdigest()
    )

    client.connect(broker)
    client.loop_start() 

    for data_portion in process_file(folder_path, filename):
        for item in data_portion:
            client.publish(f"rnx/data/{filename[:3]}", item)
            # print(item, flush=True)

    client.disconnect()
    client.loop_stop()