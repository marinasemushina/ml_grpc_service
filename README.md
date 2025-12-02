# ML gRPC Service

Минимальный ML-сервис с gRPC API для предсказаний.

## Структура проекта

```
ml_grpc_service/
├── protos/                      # Protobuf файлы
│   ├── model.proto              # gRPC контракт
│   ├── model_pb2.py             # Сгенерированный код
│   └── model_pb2_grpc.py        # Сгенерированный код
├── server/                      # gRPC сервер
│   └── server.py                # Реализация сервера
├── client/                      # gRPC клиент
│   └── client.py                # Клиент для тестирования
├── models/                      # ML модели
├── requirements.txt             # Зависимости Python
├── Dockerfile                   # Конфигурация Docker
├── .dockerignore               # Исключения для Docker
├── create_model.py             # Создание тестовой модели
├── generate_proto.py           # Генерация protobuf файлов
└── README.md                   # Документация
```

## API Endpoints

### Health Check
- **Endpoint**: `/mlservice.v1.PredictionService/Health`
- **Request**: `{}`
- **Response**: 
```json
{
  "status": "ok",
  "model_version": "v1.0.0"
}
```

### Predict
- **Endpoint**: `/mlservice.v1.PredictionService/Predict`
- **Request**: 
```json
{
  "features": [5.1, 3.5, 1.4, 0.2]
}
```
- **Response**: 
```json
{
  "prediction": "0",
  "confidence": 1.0,
  "model_version": "v1.0.0"
}
```

## Установка и запуск

### 1. Локальная установка
```bash
# Установите зависимости
pip install -r requirements.txt

# Создайте тестовую модель
python create_model.py

# Сгенерируйте protobuf файлы
python generate_proto.py

# Запустите сервер
python -m server.server
```

### 2. Тестирование
```bash
# В другом терминале запустите клиент
python -m client.client
```

### 3. Docker
```bash
# Соберите образ
docker build -t grpc-ml-service .

# Запустите контейнер
docker run -p 50051:50051 grpc-ml-service
```

## Результаты тестирования

```
Подключаемся к серверу: localhost:50051

1. Тестируем /health эндпоинт:
   Ответ Health: status=ok, version=v1.0.0

2. Тестируем /predict эндпоинт:
   Ответ Predict:
     Prediction: 0
     Confidence: 1.000
     Model Version: v1.0.0
```

## Переменные окружения

- `PORT` - порт сервера (по умолчанию: 50051)
- `MODEL_PATH` - путь к файлу модели (по умолчанию: models/model.pkl)
- `MODEL_VERSION` - версия модели (по умолчанию: v1.0.0)

## Скриншоты работы

Результаты тестирования доступны в папке [screenshots/](screenshots/)
