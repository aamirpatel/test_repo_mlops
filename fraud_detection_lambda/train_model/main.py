from src.logger import get_logger
from src.preprocess import preprocess_data
from src.train import train_model

import boto3
import pandas as pd
import io

def main():
    logger = get_logger(__name__)
    logger.info("Initialize setup...")

    # Load data from s3
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket="lambda-code-bucket-ddd", Key="upload/transaction_samples.csv")
    df = pd.read_csv(io.BytesIO(obj["Body"].read()))
    logger.info("Data loaded from s3 bucket successfully.")

    # Preprocess
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df)
    logger.info("Preprocessing completed successfully.")

    # Train and log
    metrics = train_model(X_train, X_test, y_train, y_test, scaler, logger, s3)
    logger.info("Model saved in s3 bucket as .pkl file.")

if __name__ == "__main__":
    main()
