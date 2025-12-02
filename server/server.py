import grpc
from concurrent import futures
import pickle
import os
import numpy as np
from typing import Tuple
import logging
from datetime import datetime
import sys

# Добавляем путь к protos в начало
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'protos'))

# Теперь импортируем protobuf файлы
import model_pb2
import model_pb2_grpc

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLModel:
    """Класс для работы с ML моделью"""
    
    def __init__(self, model_path: str, version: str):
        self.model_path = model_path
        self.version = version
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Загрузка модели из файла"""
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            logger.info(f"Модель загружена: {self.model_path}, версия: {self.version}")
        except Exception as e:
            logger.error(f"Ошибка загрузки модели: {e}")
            raise
    
    def predict(self, features: list) -> Tuple[str, float]:
        """
        Предсказание на основе признаков
        
        Args:
            features: список признаков
            
        Returns:
            tuple: (предсказание, уверенность)
        """
        try:
            # Преобразуем признаки в numpy array
            features_array = np.array(features).reshape(1, -1)
            
            # Получаем предсказание и вероятность
            if hasattr(self.model, 'predict_proba'):
                proba = self.model.predict_proba(features_array)[0]
                prediction_idx = np.argmax(proba)
                confidence = float(proba[prediction_idx])
                prediction = str(prediction_idx)
            else:
                # Для моделей без predict_proba
                prediction = str(self.model.predict(features_array)[0])
                confidence = 0.9  # Значение по умолчанию
            
            return prediction, confidence
        except Exception as e:
            logger.error(f"Ошибка предсказания: {e}")
            raise

class PredictionServicer(model_pb2_grpc.PredictionServiceServicer):
    """gRPC сервис для предсказаний"""
    
    def __init__(self):
        # Получаем переменные окружения
        model_path = os.getenv('MODEL_PATH', 'models/model.pkl')  
        model_version = os.getenv('MODEL_VERSION', 'v1.0.0')
        
        # Инициализируем модель
        self.ml_model = MLModel(model_path, model_version)
    
    def Health(self, request, context):
        """Эндпоинт здоровья сервиса"""
        logger.info("Health check requested")
        return model_pb2.HealthResponse(
            status="ok",
            model_version=self.ml_model.version
        )
    
    def Predict(self, request, context):
        """Эндпоинт для предсказаний"""
        try:
            logger.info(f"Predict requested with {len(request.features)} features")
            
            # Проверяем наличие признаков
            if not request.features:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("No features provided")
                return model_pb2.PredictResponse()
            
            # Получаем предсказание
            prediction, confidence = self.ml_model.predict(request.features)
            
            logger.info(f"Prediction: {prediction}, Confidence: {confidence}")
            
            return model_pb2.PredictResponse(
                prediction=prediction,
                confidence=confidence,
                model_version=self.ml_model.version
            )
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return model_pb2.PredictResponse()

def serve():
    """Запуск gRPC сервера"""
    # Получаем порт из переменных окружения
    port = os.getenv('PORT', '50051')
    
    # Создаем сервер
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_PredictionServiceServicer_to_server(
        PredictionServicer(), server
    )
    
    # Запускаем сервер
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.info(f"Server started on port {port}")
    logger.info(f"Model path: {os.getenv('MODEL_PATH', 'models/model.pkl')}")
    logger.info(f"Model version: {os.getenv('MODEL_VERSION', 'v1.0.0')}")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Server stopping...")
        server.stop(0)

if __name__ == '__main__':
    serve()
