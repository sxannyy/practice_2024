import asyncio
from datetime import date, timedelta
import json
import paho.mqtt.client as mqtt_client
import subprocess
import os
import requests
from logger_settings import logger


async def run_command(command):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        print(f"Error running command {command}: {stderr.decode().strip()}")
        logger.error(f"Error running command {command}: {stderr.decode().strip()}")
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
            logger.warning(f"Directory {directory} does not exist.")
            return

        os.system('sudo rm /etc/systemd/system/publisher_*')

    except Exception as e:
        print(f"An error occurred: {e}")

async def create_services():
    await run_command(f'sudo python3 ./rnx/create_services.py {(date.today() - timedelta(days=3, weeks=25)).strftime("%Y-%d-%m")}')

def get_pub_names(date: date):
    files = os.listdir(f'/home/ivan/praktika/data/{date}')
    return [names[:3] for names in files]

def register(name: str, surname: str, email: str, password: str):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    user_data = {
    "name": name,
    "surname": surname,
    "email": email,
    "password": password
    }

    response = requests.post('http://0.0.0.0:8000/user/create_user/', headers=headers, data=json.dumps(user_data))
    return response

def login(email: str, password: str):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': '',
        'username': email,
        'password': password,
        'scope': '',
        'client_id': '',
        'client_secret': ''
    }
    response = requests.post('http://0.0.0.0:8000/login/token', headers=headers, data=data)
    
    return response

def get_user(token):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.get('http://0.0.0.0:8000/user/get_user_id/', headers=headers)

    return response

def subscribe(token, topic: str):
    url = f'http://0.0.0.0:8000/user/subscribe/?subscription={topic}'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.patch(url, headers=headers)
    if response.status_code == 404 or response.status_code == 422:
        return False
    
    return True

def unsubscribe(token, topic: str):
    url = f'http://0.0.0.0:8000/user/unsubscribe/?subscription={topic}'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.patch(url, headers=headers)
    if response.status_code == 404 or response.status_code == 422 or response.status_code == 503:
        print(response.json())
        return False
 
    return True

def get_user_topics(token):
    url = 'http://0.0.0.0:8000/user/get_all_user_subs/'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        print(response['detail'])
    return response

def get_streams(token, client: mqtt_client.Client):
    url = 'http://0.0.0.0:8000/user/get_all_user_subs/'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        print(response['detail'])
    
    print('Получение потока:')
    print(response.json())
    for topic in response.json()['subscription'].split(', '):
        client.subscribe(f"rnx/data/{topic}")

def show_topics(token):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.get('http://0.0.0.0:8000/user/get_topics/', headers=headers)

    return response.json()['topic_names']
