# Проектная работа 9 спринта. Проект по тестированию CI

Приложение на FastAPI и развернутым кластером MongoDB, состоящим  из двух шардов (наборы реплик по три узла), серверов конфигурации (три узла реплик) и двух маршрутизаторов Mongos.

Приложение позволяет смотреть статистику оценок, выставленных пользователями конкретному фильму.

## Запуск приложения
Клонируйте текущий репозиторий
```
git clone https://github.com/aleksioprime/ugc_sprint_2.git
```
Запустите из корневой папки проекта Docker-Сompose:
```
docker-compose -p practicum_rating up -d
```

## Проверка запуска приложения и кластера MongoDB
Проверка запуска сервера приложения
```
http://localhost:82/api/v1/ping/
```
Проверка взаимодействия приложения с кластером MongoDB
```
http://localhost:82/api/v1/ping/mongo
```

## Генерация данных и проверка API
После запуска основного приложения можно сгенерировать данные. Для этого необходимо запустить программу в папке generation, указав данные в аргументах запуска.
Запускать можно в виртуальной среде с установленными библиотеками из файла `generation/requirements.txt`:
```
python generation/main.py --mongo-url "mongodb://localhost:27019" --count-users 5000 --count-movies 1000 --count-ratings 20000 
```
Для очистки всех данных можно использовать команду:
```
python generation/main.py --mongo-url "mongodb://localhost:27019" --clear
```
Посмотреть данные в MongoDB можно с помощью программы [MongoDB Compass](https://www.mongodb.com/try/download/compass) или утилиты командной строки [mongoShell](https://www.mongodb.com/docs/mongodb-shell/install/):
```shell
mongosh mongodb://localhost:27019
show dbs
use ugc
db.getCollectionNames()
db.movies.aggregate([{ $sample: { size: 1 } }])
quit
```
Для вывода оценок этого фильма по API скопируйте из предыдущего результата его ID и перейдите по адресу:
```
http://localhost:82/api/v1/ratings/movie/<uuid_фильма>/
```

## Выполнение тестов
```
docker-compose -f app/tests/functional/docker-compose.yaml -p practicum_rating_test up --build --abort-on-container-exit
```

### Удаление контейнеров и томов после тестов
```
docker-compose -f app/tests/functional/docker-compose.yaml -p practicum_test down -v
docker image prune -f
```

## Настройка вывода сообщений CI в Telegram

1. Зарегистрируйте бота в Telegram
```shell
/start
/newbot
<название бота>
<username бота>
```

2. Скопируйте полученный токен (например, `123456789:ABCDefGhIJKlmnopQRStUvWxYZ1234567890`) и добавьте его в Github SECRET под именем `TELEGRAM_TOKEN`
3. Найдите созданного бота и отправьте ему любое сообщение
4. Откройте в браузере ссылку `https://api.telegram.org/bot<TELEGRAM_TOKEN>/getUpdates`
5. Из полученного JSON скопируйте ID чата (`message.chat.id`)
```
{
  "update_id": 123456789,
  "message": {
    "chat": {
      "id": 987654321,
      "first_name": "YourName",
      "type": "private"
    }
  }
}
```
6. Добавте ID чата в Github SECRET под именем `TELEGRAM_CHAT_ID`