import os
import sys
import joblib
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import MODEL_URI, MLFLOW_TRACKING_URI

# 경로 설정
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "spam.csv")
ARTIFACT_DIR = os.path.join(BASE_DIR, "artifacts")
MODEL_PATH = os.path.join(ARTIFACT_DIR, "spam_model.joblib")

os.makedirs(ARTIFACT_DIR, exist_ok=True)

# MLflow 실험 세팅
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("spam-classification-local")

# 데이터 로드
df = pd.read_csv(DATA_PATH)
X = df["text"]
y = df["label"]

# 파이프라인 구성
pipeline = Pipeline([
    ("vectorizer", CountVectorizer()),
    ("classifier", LogisticRegression(max_iter=200))
])

# MLflow 실험 기록 시작
with mlflow.start_run():
    # 1. 파라미터 기록 (Hyperparameters & Metadata)
    mlflow.log_param("model_type", "LogisticRegression")
    mlflow.log_param("vectorizer", "CountVectorizer")
    mlflow.log_param("max_iter", 200)
    mlflow.log_param("data_path", DATA_PATH)
    mlflow.log_param("row_count", len(df))

    # 2. 모델 학습
    pipeline.fit(X, y)

    # 3. 성능 지표 기록 (Metrics)
    preds = pipeline.predict(X)
    acc = accuracy_score(y, preds)
    mlflow.log_metric("train_accuracy", acc)

    # 4. 모델 파일 저장 및 Artifact 기록
    joblib.dump(pipeline, MODEL_PATH)
    mlflow.log_artifact(DATA_PATH)    # 원본 데이터 로깅
    mlflow.log_artifact(MODEL_PATH)  # 저장된 joblib 파일 로깅

    # 5. MLflow Model Format으로 저장 (서빙 및 재사용 용이)
    mlflow.sklearn.log_model(pipeline, name="model", registered_model_name="spam-model")

    print(f"Model saved to: {MODEL_PATH}")
    print(f"Train Accuracy: {acc:.4f}")