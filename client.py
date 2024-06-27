from datetime import datetime
from hashlib import md5
import time
import paho.mqtt.client as mqtt_client

broker = "broker.emqx.io"

def on_message(client, userdata, message):
    global last_message_time
    last_message_time = datetime.now()
    sender_id = message.mid
    time.sleep(0.1)
    data = str(message.payload.decode("utf-8"))
    print(data)

#TODO: Все взаимодействия с fastapi

client = mqtt_client.Client(
   mqtt_client.CallbackAPIVersion.VERSION1, 
   md5(str(datetime.now()).encode('utf-8')).hexdigest()
)

#TODO: Получение потока

client.on_message=on_message
client.connect(broker) 
client.loop_start()
client.subscribe("rnx/data/ABP")
time.sleep(1800)
client.disconnect()
client.loop_stop()