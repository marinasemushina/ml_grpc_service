import grpc
import sys
import os

# Добавляем путь к protos
current_dir = os.path.dirname(os.path.abspath(__file__))
protos_path = os.path.join(current_dir, '..', 'protos')
sys.path.insert(0, protos_path)

import model_pb2
import model_pb2_grpc

def run():
    """Запуск клиента для тестирования сервера"""
    
    # Параметры подключения
    server_address = 'localhost:50051'
    
    try:
        # Создаем канал и stub
        channel = grpc.insecure_channel(server_address)
        stub = model_pb2_grpc.PredictionServiceStub(channel)
        
        print(f"Подключаемся к серверу: {server_address}")
        
        # Тестируем Health endpoint
        print("\n1. Тестируем /health эндпоинт:")
        try:
            health_response = stub.Health(
                model_pb2.HealthRequest(),
                timeout=5
            )
            print(f"   Ответ Health: status={health_response.status}, "
                  f"version={health_response.model_version}")
        except grpc.RpcError as e:
            print(f"   Ошибка Health: {e.code()}")
            return
        
        # Тестируем Predict endpoint
        print("\n2. Тестируем /predict эндпоинт:")
        
        # Пример признаков (замените на реальные для вашей модели)
        # Для примера используем 4 признака
        features = [5.1, 3.5, 1.4, 0.2]
        
        try:
            predict_response = stub.Predict(
                model_pb2.PredictRequest(features=features),
                timeout=5
            )
            print(f"   Ответ Predict:")
            print(f"     Prediction: {predict_response.prediction}")
            print(f"     Confidence: {predict_response.confidence:.3f}")
            print(f"     Model Version: {predict_response.model_version}")
        except grpc.RpcError as e:
            print(f"   Ошибка Predict: {e.code()} - {e.details()}")
            
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    run()
