from sklearn.linear_model import LogisticRegression
from src.evaluate import evaluate_model

import mlflow
import mlflow.sklearn
import pickle
import boto3
import io

def train_model(X_train, X_test, y_train, y_test, scaler, logger, s3):
    with mlflow.start_run():

        logger.info("Starting model training...")

        model = LogisticRegression()
        model.fit(X_train, y_train)
        logger.info("Model training completed.")

        # Evaluate
        metrics = evaluate_model(model, X_test, y_test, logger)
        logger.info("Model evaluation completed.")

        # Log model to MLflow
        mlflow.sklearn.log_model(model, artifact_path="sklearn-model")
        logger.info("Model logged to MLflow.")

        # Log metrics to MLflow
        for key, value in metrics.items():
            mlflow.log_metric(key, value)
            logger.info(f"MLflow metric logged: {key} = {value:.4f}")

        # Log scaler params
        if scaler:
            mlflow.log_dict(scaler.get_params(), artifact_file="scaler_params.json")
            logger.info("Scaler parameters logged to MLflow.")

        # Save model to S3 as model.pkl and scaler.pkl
        model_buffer = io.BytesIO()
        pickle.dump(model, model_buffer)
        model_buffer.seek(0)
        s3.put_object(Bucket="lambda-code-bucket-ddd", Key="model/model.pkl", Body=model_buffer.getvalue())
        logger.info(f"Model .pkl saved to S3")

        # Save scaler to S3
        scaler_buffer = io.BytesIO()
        pickle.dump(scaler, scaler_buffer)
        scaler_buffer.seek(0)
        s3.put_object(Bucket="lambda-code-bucket-ddd", Key="model/scaler.pkl", Body=scaler_buffer.getvalue())
        logger.info(f"Scaler .pkl saved to S3 at s3")

    return metrics
