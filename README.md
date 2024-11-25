# Проектная работа 9 спринта. Проект по тестированию CI

## Для ревьюера
1) [логирование_1](https://github.com/NankuF/ugc_sprint_1/commit/0f56ee1c39f6f235b0a552ec372370848f9b3483)<br>
2) [логирование_2](https://github.com/NankuF/Async_API_sprint_1/commit/c56d5f4f1c1d31e5af3a16e1fe50b5f1d7b0f2ac)<br>
3) **В этом репозитории - CI/CD, исследование и API.**<br>
----

Приложение на FastAPI и c развернутым кластером MongoDB, состоящим  из двух шардов (наборы реплик по три узла), серверов конфигурации (три узла реплик) и двух маршрутизаторов Mongos.

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
docker-compose -f app/tests/functional/docker-compose.yaml -p practicum_rating_test down -v
docker image prune -f
```

## Исследование
```
docker-compose -f research/docker-compose.yaml -p practicum_research up --build --abort-on-container-exit
```
В приложении выполняется исследование скорости записи и чтения из двух хранилищ: MongoDB и Postgres.
Результаты исследования выводятся в файл [results.md](./research/app/results.md)

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
6. Добавьте ID чата в Github SECRET под именем `TELEGRAM_CHAT_ID`