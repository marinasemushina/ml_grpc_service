import pickle
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os

# Создаем директорию models
os.makedirs("models", exist_ok=True)

# Загружаем данные
iris = load_iris()
X, y = iris.data, iris.target

# Делим на train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Обучаем модель
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Сохраняем модель
with open('models/model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Модель сохранена в models/model.pkl")
print(f"Точность на тестовых данных: {model.score(X_test, y_test):.3f}")
