import sys
import zipfile
import requests
from datetime import date, datetime, timedelta
import os
import asyncio
import shutil
from functions import run_command


data_dir = './data/'


def delete_everything_in_folder(folder_path):
    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
        os.mkdir(folder_path)


async def decompress_all_data(directory):
    await run_command(f"gunzip {data_dir}{directory}*.crx.gz; gunzip {data_dir}{directory}*.24d.Z")
    files = os.listdir(data_dir + directory)
    tasks = []
    for file in files:
        filename = file.split('.')[0]
        if file.endswith('.24d'):
            command = f"./CRX2RNX {data_dir}{directory}{filename}.24d"
        else:
            command = f"./CRX2RNX {data_dir}{directory}{filename}.crx"
        tasks.append(run_command(command))
    
    await asyncio.gather(*tasks)
    
    await run_command(f"rm {data_dir}{directory}*.crx; rm {data_dir}{directory}*.24d")


def unzip_and_delete(zip_path, extract_to):
    if not os.path.isfile(zip_path):
        print(f"Файл {zip_path} не существует.")
        return

    if not os.path.isdir(extract_to):
        os.makedirs(extract_to)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        # print(f"Файл {zip_path} успешно разархивирован в {extract_to}.")

    os.remove(zip_path)
    # print(f"Файл {zip_path} успешно удален.")


async def download_info(date: date):
    delete_everything_in_folder(f'{data_dir}{(date - timedelta(days=6)).strftime("%Y-%d-%m")}')
    date = date.strftime("%Y-%d-%m")
    directory = f"{date}/"

    if not os.path.isdir(f"{data_dir}{directory}"):
        os.mkdir(f"{data_dir}{directory}")

    link = f"https://api.simurg.space/datafiles/map_files?date={date}"
    file_name = f"{data_dir}{directory}{date}.zip"
    with open(file_name, "wb") as f:
        print("Downloading %s" % file_name)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
                sys.stdout.flush()

    unzip_and_delete(f"{data_dir}{directory}{date}.zip",f"{data_dir}{directory}")
    # await run_command(f"unzip {data_dir}{directory}{date}.zip -d {data_dir}{directory}")
    # await run_command(f"rm {data_dir}{directory}{date}.zip")
    await decompress_all_data(directory)

async def get_info():
    await download_info(date.today() - timedelta(days=5))

