from datetime import datetime
from hashlib import md5
import time
import paho.mqtt.client as mqtt_client
from rnx.functions import *
from logger_settings import logger

broker = "broker.emqx.io"

def on_message(client, userdata, message):
    global last_message_time
    last_message_time = datetime.now()
    sender_id = message.mid
    time.sleep(0.1)
    data = str(message.payload.decode("utf-8"))
    print(data)

response = register('lolov', 'lolik', 'lol@example.com', '1234')
if response.status_code != 200:
    print('Ошибка регистрации!')
    logger.error('Ошибка регистрации!')
    exit(1)
response = login('lol@example.com', '1234')
if response.status_code != 200:
    print('Ошибка логина!')
    logger.error('Ошибка логина!')
    exit(1)
token = response.json()['access_token']
user_id = get_user(token).json()['user_id']

client = mqtt_client.Client(
   mqtt_client.CallbackAPIVersion.VERSION1, 
   user_id
)

print(show_topics(token))

for name in ['CCJ', 'CED', 'CHP']:
    if not subscribe(token, name):
        print('Не подписалось!')
        logger.error('Не подписалось!')
        exit(2)
if not unsubscribe(token, 'CCJ'):
    print('Не отписалось!')
    logger.error('Не отписалось!')
    exit(2)

client.on_message=on_message
client.connect(broker) 
client.loop_start()
get_streams(token, client)
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()