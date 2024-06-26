import asyncio
from datetime import date, timedelta
import subprocess
import os


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

def run_asyncio_job(job):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(job())
    loop.close()

def delete_publisher_services(directory='/etc/systemd/system'):
    try:
        # Проверяем, что директория существует
        if not os.path.exists(directory):
            print(f"Directory {directory} does not exist.")
            return

        # Получаем список всех файлов в директории
        files = os.listdir(directory)

        # Фильтруем файлы, которые начинаются с "publisher"
        publisher_services = [f for f in files if f.startswith('publisher')]

        # Удаляем файлы
        for service in publisher_services:
            file_path = os.path.join(directory, service)
            if os.path.isfile(file_path):
                os.system(f'sudo systemctl stop {service}')
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            else:
                print(f"Skipping {file_path}, not a file.")

    except Exception as e:
        print(f"An error occurred: {e}")


def create_services():
    run_command(f'sudo create_services.py {(date.today() - timedelta(days=2)).strftime("%Y-%d-%m")}')