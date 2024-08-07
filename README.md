# Приложение для отслеживания обновлений GNSS-приемника
Данное приложение было создано во время летней технологической практики в 2024 году. Оно необходимо для отслеживания публикаций данных GNSS-приемников, которые транслируются со спутников.

## Системные требования
Нами был разработан скрипт для загрузки всех необходимых фреймворков и библиотек. Далее в инструкции Вы с этим ознакомитесь.
Рекомендуемая ОС: Ubuntu 22.04.

## Как это работает?
Существует приложение, которое взаимодействует с пользователем через ввод данных с клавиатуры. Данное приложение отправляет команды всей разработанной системе. В нашем проекте также создаются запросы на фреймворке FastAPI, представляющие из себя обработку данных. К приложению подключена база данных на PostgreSQL для удобства работы с информацией о пользователях. Также в проекте осуществлена система типа "издатель-подписчик", где в роли издателя выступают приемники, а в роли подписчиков - пользователи.

## Архитектура приложения, реализованная в диаграмме
![alt text](https://i.ibb.co/wdkxQJt/diagramoftheproject.png)

## Сценарии использования:
  - Регистрация/вход пользователя;
  - Подписка/отписка на приемник;
  - Выдача/отключение администраторских способностей (только на FastAPI);
  - Получение списка всех активных приемников;
  - Получение списка приемников с осуществленной подпиской;
  - Получение публикаций.
    
## FastAPI
  - Запрос на регистрацию пользователя. Параметры: имя, фамилия, адрес почты, пароль;
  - Запрос на вход пользователя. Параметры: адрес почты, пароль;
  - Запрос на вывод профиля определенного пользователя. Параметры: ID профиля, токен сессии (передается автоматически);
  - Запрос на удаление профиля пользователя. Параметры: ID профиля, токен сессии (передается автоматически);
  - Запрос на обновление профиля пользователя. Параметры: ID профиля, желаемые изменения, токен сессии (передается автоматически);
  - Запрос на выдачу/отзыв привилегий администратора. Параметры: ID профиля, токен сессии (передается автоматически);
  - Запрос на подписку/отписку на определенный приемник. Параметры: название приемника (состоящее из 3-х букв на латинице), токен сессии (передается автоматически);
  - Запрос на вывод ID пользователя. Параметры: токен сессии (передается автоматически);
  - Запрос на вывод всех приемников. Параметры: токен сессии (передается автоматически);
  - Запрос на вывод приемников с осуществленной подпиской. Параметры: ID профиля, токен сессии (передается автоматически);
  - Запрос на вывод пользователей с осуществленной подпиской на определенный приемник. Параметры: название приемника (состоящее из 3-х букв на латинице), токен сессии (передается автоматически).

## Система "издатель-подписчик"
Данная система генерирует публикации от лица издателей-приемников для подписчиков-пользователей. Топики для каждого издателя-приемника формируются из первых 3-х букв имени файлов скачанного RNX-архива.

## Скрипты перевода полученного архива в RNX-файлы
Для этого скрипта использовалась программа CRX2RNX за авторством Yuki Hatanaka. Ссылки на источники: https://www.gsi.go.jp/ENGLISH/Bulletin55.html и https://terras.gsi.go.jp/ja/crx2rnx.html. 

## Настройка и установка проекта:
При необходимости прописать в командной строке ```chmod +x ./scripts/<script_name>.sh``` для всех скриптов!

### Для установки всех библиотек python и linux:
Пропишем в папке проекта:
```
pip install .
./scripts/configure.sh
```

### Для поднятия сервисов баз для локальной разработки нужно запустить команду:
```
sudo make up
```

### Создание миграций и настройка alembic:
Для этого написан специальный скрипт, который запускается из папки проекта командой:
```
./scripts/init.sh
```

### Внимание! Если порт занят или необходимо почистить миграции воспользуйтесь:
```
./scripts/clear_port.sh
./scripts/delete.sh
```

### Для поднятия FastAPI:
В папке проекта рекомендуется прописать следующую команду:
```
python3 main.py
```

### Для запуска скрипта-планировщика:
```
sudo python3 ./rnx/scheduler.py
```

### Для запуска клиент-приложения пропишите в папке проекта:
```
python3 client.py
```
