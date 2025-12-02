# ML gRPC Service

Минимальный ML-сервис с gRPC API для предсказаний.

## Структура проекта
'''
ml_grpc_service/
├── protos/ # Protobuf файлы
├── server/ # gRPC сервер
├── client/ # gRPC клиент для тестирования
├── models/ # ML модели
├── Dockerfile # Конфигурация Docker
├── requirements.txt # Зависимости Python
└── README.md # Документация
'''

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
Predict
Endpoint: /mlservice.v1.PredictionService/Predict

Request:
{
  "features": [5.1, 3.5, 1.4, 0.2]
}
Response:
{
  "prediction": "1",
  "confidence": 0.92,
  "model_version": "v1.0.0"
}

