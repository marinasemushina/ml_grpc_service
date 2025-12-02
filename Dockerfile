FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем переменные окружения
ENV PORT=50051 \
    MODEL_PATH=/app/models/model.pkl \
    MODEL_VERSION=v1.0.0 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Создаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем ВСЕ файлы (включая модели)
COPY . .

# Создаем директорию для моделей
RUN mkdir -p /app/models

# Создаем модель прямо в контейнере
RUN python create_model.py

# Генерируем protobuf файлы
RUN python generate_proto.py

# Проверяем что модель создалась
RUN ls -la /app/models/

# Экспортируем порт
EXPOSE 50051

# Запускаем сервер
CMD ["python", "-m", "server.server"]
