# Проектная работа 9 спринта. Проект по тестированию CI

Приложение позволяет смотреть статистику оценок, выставленных пользователями конкретному фильму по эндпойнту:

```
http://localhost:82/api/v1/ratings/movie/<uuid>/
```

## Запуск приложения
Скачайте текущий репозиторий
```
https://github.com/aleksioprime/ugc_sprint_2.git
```
Запустите docker-compose:
```
docker-compose -p practicum_rating up -d
```
Примечание: во время запуска будет создан и настроен кластер MongoDB. Для проверки и просмотра базы можно подключиться через программ **Compass** или утилиту командной строки **mongosh** по адресу `mongodb://localhost:27019`

## Генерация данных
Для генерации данных нужно запустить программу в папке generation, указав данные в аргументах запуска:
```
python generation/main.py --count-users 5000 --count-movies 1000 --count-ratings 20000 --mongo-url "mongodb://my-mongo-host:27017"
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

1. Зарегистрируйте бота в Telegram

```shell
/start
/newbot
<имя бота>
<имя бота>
```

2. Скопировать токен, например 123456789:ABCDefGhIJKlmnopQRStUvWxYZ1234567890, и добавить в SECRET в Github под именем TELEGRAM_TOKEN
3. Найти бота и отправить ему любое сообщение
4. Открыть в браузере ссылку `https://api.telegram.org/bot<TELEGRAM_TOKEN>/getUpdates`
5. Из полученного JSON скопировать id чата
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
6. Добавить ID чата в в SECRET в Github под именем TELEGRAM_CHAT_ID