import os
MODEL_MODE = "ml" # "rules"
# LOCAL_MODEL_PATH = "ml/artifacts/spam_model.joblib"
MLFLOW_TRACKING_URI="sqlite:///mlflow.db"
# MODEL_URI = "runs:/74d98b014c5b4d9e80ef7dc964863e53/model"
MODEL_URI = "models:/spam-model@champion"