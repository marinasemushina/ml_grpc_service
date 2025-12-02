#!/usr/bin/env python3
"""Генерация Python кода из .proto файлов"""

import subprocess
import os
import sys

def main():
    # Создаем директорию protos, если она не существует
    os.makedirs("protos", exist_ok=True)
    
    # Используем sys.executable вместо "python"
    cmd = [
        sys.executable,  # ← ИСПРАВЛЕНО: используем текущий интерпретатор Python
        "-m", "grpc_tools.protoc",
        "-Iprotos",
        "--python_out=protos",
        "--grpc_python_out=protos",
        "protos/model.proto"
    ]
    
    print("Генерация Python кода из .proto файлов...")
    try:
        subprocess.run(cmd, check=True)
        print("Генерация завершена успешно!")
        print("Созданы файлы: protos/model_pb2.py и protos/model_pb2_grpc.py")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при генерации: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Команда не найдена: {cmd}")
        print("Убедитесь что grpcio-tools установлены")
        sys.exit(1)

if __name__ == "__main__":
    main()
