import sys
import requests
from datetime import date
import subprocess
import os
import asyncio
import shutil

directory = "./data/"

def delete_everything_in_folder(folder_path):
    shutil.rmtree(folder_path)
    os.mkdir(folder_path)


async def run_command(command):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        print(f"Error running command {command}: {stderr.decode().strip()}")
    return stdout, stderr

async def decompress_all_data():
    files = os.listdir(directory)
    
    command = f"gunzip {directory}*.crx.gz"
    await run_command(command)

    tasks = []
    
    for file in files:
        if file.endswith('.Z'):
            continue
        filename = file.split('.')[0]
        command = f"./CRX2RNX {directory}{filename}.crx"
        tasks.append(run_command(command))
    
    await asyncio.gather(*tasks)
    
    command = f"rm {directory}*.crx"
    await run_command(command)


async def download_info(date: date):
    delete_everything_in_folder(f'{directory}')

    date = date.strftime("%Y-%d-%m")

    link = f"https://api.simurg.space/datafiles/map_files?date={date}"
    file_name = f"{directory}{date}.zip"
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
    await run_command(f"unzip {directory}{date}.zip -d {directory}; rm -r {directory}{date}.zip")

# asyncio.run(decompress_all_data()) - запуск функции асинхронно
