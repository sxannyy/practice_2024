from gnss_tec import rnx
import time
import os
import sys

def process_file(folder_path, filename):
    with open(f'{folder_path}/{filename}.rnx') as obs_file:
        reader = rnx(obs_file)
        prev_epoch = None
        data = []
        prev_system_time = time.time()
        make_sleep = False
        for tec in reader:
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

    for data_portion in process_file(folder_path, filename):
        for item in data_portion:
            print(item, flush=True)
