from datetime import datetime
from hashlib import md5
import time
import paho.mqtt.client as mqtt_client
from rnx.functions import (register,
    login,
    get_user,
    show_topics,
    subscribe,
    unsubscribe,
    get_user_topics,
    get_streams)
from logger_settings import logger

broker = "broker.emqx.io"

def on_message(client, userdata, message):
    global last_message_time
    last_message_time = datetime.now()
    sender_id = message.mid
    time.sleep(0.1)
    data = str(message.payload.decode("utf-8"))
    print(data)

def main():
    token = ""
    client = None
    
    def register_user():
        name = input("Введите имя: ")
        surname = input("Введите фамилия: ")
        email = input("Введите email: ")
        password = input("Введите пароль: ")
        response = register(name, surname, email, password)
        if response.status_code != 200:
            print('Ошибка регистрации!')
            logger.error('Ошибка регистрации!')
        else:
            print('Регистрация успешна!')

    def login_user():
        nonlocal token, client
        email = input("Введите email: ")
        password = input("Введите пароль: ")
        response = login(email, password)
        if response.status_code != 200:
            print('Ошибка логина!')
            logger.error('Ошибка логина!')
        else:
            token = response.json()['access_token']
            user_id = get_user(token).json()['user_id']
            client = mqtt_client.Client(
                mqtt_client.CallbackAPIVersion.VERSION1, 
                user_id
            )
            client.on_message = on_message
            client.connect(broker)
            client.loop_start()
            print('Логин успешен!')

    def list_topics():
        if token:
            topics = show_topics(token)
            print("Все топики:")
            for topic in topics:
                print(topic)
        else:
            print("Сначала войдите в систему.")

    def subscribe_topic():
        if token:
            topic = input("Введите имя топика для подписки: ")
            if subscribe(token, topic):
                print(f'Подписка на {topic} успешна!')
            else:
                print('Не удалось подписаться на топик.')
                logger.error('Не удалось подписаться на топик.')
        else:
            print("Сначала войдите в систему.")

    def unsubscribe_topic():
        if token:
            topic = input("Введите имя топика для отписки: ")
            if unsubscribe(token, topic):
                print(f'Отписка от {topic} успешна!')
            else:
                print('Не удалось отписаться от топика.')
                logger.error('Не удалось отписаться от топика.')
        else:
            print("Сначала войдите в систему.")

    def list_user_topics():
        if token:
            topics = get_user_topics(token)
            print("Ваши подписки:")
            for topic in topics.json()['subscription'].split(', '):
                print(topic)
        else:
            print("Сначала войдите в систему.")

    def display_stream():
        if token and client:
            print("Отображение потока сообщений. Нажмите Ctrl+C для выхода.")
            get_streams(token, client)
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
        else:
            print("Сначала войдите в систему и подключитесь к брокеру.")

    actions = {
        '1': register_user,
        '2': login_user,
        '3': list_topics,
        '4': subscribe_topic,
        '5': unsubscribe_topic,
        '6': list_user_topics,
        '7': display_stream,
    }

    print("Консольный клиент запущен. Нажмите Ctrl+C для выхода.")
    try:
        while True:
            print("\nВыберите действие:")
            print("1. Регистрация")
            print("2. Вход")
            print("3. Получить список всех топиков")
            print("4. Подписаться на топик")
            print("5. Отписаться от топика")
            print("6. Получить топики, на которые подписан пользователь")
            print("7. Отображение потока сообщений")
            choice = input("Введите номер действия: ")

            action = actions.get(choice)
            if action:
                action()
            else:
                print("Неверный выбор. Пожалуйста, введите номер от 1 до 7.")
    except KeyboardInterrupt:
        if client:
            client.disconnect()
            client.loop_stop()
        print("\nВыход из программы.")

if __name__ == "__main__":
    main()
