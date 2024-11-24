# Указываем базовый образ
FROM --platform=linux/amd64 python:3.11.3-buster

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY ./app /app

# Устанавливаем зависимости
COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Указываем команду по умолчанию
CMD ["python", "main.py", "--storage", "postgres"]