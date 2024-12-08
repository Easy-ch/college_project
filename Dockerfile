FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только папку app и requirements.txt
COPY app /app
COPY requirements.txt /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт 8000
EXPOSE 8000

# Указываем команду для запуска
CMD ["python", "main.py"]
