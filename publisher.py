from gnss_tec import rnx
import time
import os
import sys

def process_file(folder_path, filename):
    with open(f'{folder_path}/{filename}.rnx') as obs_file:
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

    process_file(folder_path, filename)
