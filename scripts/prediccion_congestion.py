import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

MODEL_PATH = 'models/congestion_model.pkl'

def train_and_save_model():
    # Dataset sintético
    np.random.seed(42)
    n_samples = 1000
    vehicle_count = np.random.randint(0, 101, size=n_samples)
    hour = np.random.randint(0, 24, size=n_samples)
    day_of_week = np.random.randint(0, 7, size=n_samples)

    is_peak = ((hour >= 7) & (hour <= 9)) | ((hour >= 17) & (hour <= 19))
    noise = np.random.normal(scale=10, size=n_samples)
    score = vehicle_count + (is_peak.astype(int) * 20) + noise

    congestion = np.where(score > 70, 'high', 'low')

    df = pd.DataFrame({
        'vehicle_count': vehicle_count,
        'hour': hour,
        'day_of_week': day_of_week,
        'congestion': congestion
    })

    X = df[['vehicle_count', 'hour', 'day_of_week']]
    y = df['congestion']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = DecisionTreeClassifier(max_depth=5, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"[INFO] Modelo entrenado. Accuracy: {acc:.2f}")

    joblib.dump(clf, MODEL_PATH)
    print(f"[INFO] Modelo guardado en {MODEL_PATH}")

def predict_congestion(vehicle_count, hour, day_of_week):
    if not os.path.exists(MODEL_PATH):
        print("[INFO] Modelo no encontrado. Entrenando...")
        train_and_save_model()

    clf = joblib.load(MODEL_PATH)

    data = pd.DataFrame({
        'vehicle_count': [vehicle_count],
        'hour': [hour],
        'day_of_week': [day_of_week]
    })

    prediction = clf.predict(data)[0]
    return prediction

if __name__ == "__main__":
    # Ejemplo de uso
    vehicle_count = 80
    hour = 8
    day_of_week = 1  # Lunes

    result = predict_congestion(vehicle_count, hour, day_of_week)
    print(f"[RESULT] Predicción de congestión: {result}")
