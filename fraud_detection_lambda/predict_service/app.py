import json
import joblib
import boto3
import os
import io
import numpy as np
import pandas as pd

# Constants
BUCKET_NAME = "lambda-code-bucket-ddd"
MODEL_KEY = "model/model.pkl"
SCALER_KEY = "model/scaler.pkl"

# Columns used during preprocessing
CATEGORICAL_COLS = [
    'card_type', 'merchant_category', 'transaction_type',
    'device_type', 'entry_method', 'customer_region'
]
NUMERIC_COLS = [
    'amount', 'customer_age', 'hour_of_day',
    'avg_transaction_amt_24h', 'num_prev_transactions_24h'
]
DROP_COLS = [
    "transaction_id", "timestamp", "customer_id", "merchant_id", "is_fraud"
]

# Load model and scaler from S3
def load_pickle_from_s3(bucket, key):
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket, Key=key)
    return joblib.load(io.BytesIO(response['Body'].read()))

model = load_pickle_from_s3(BUCKET_NAME, MODEL_KEY)
scaler = load_pickle_from_s3(BUCKET_NAME, SCALER_KEY)

def lambda_handler(event, context):
    try:
        # Parse input JSON
        body = json.loads(event["body"])
        input_data = pd.DataFrame([body])

        # Drop unused columns if present
        for col in DROP_COLS:
            if col in input_data.columns:
                input_data.drop(columns=col, inplace=True)

        # One-hot encode categorical columns
        # input_data = pd.get_dummies(input_data, columns=CATEGORICAL_COLS, drop_first=True)
        existing_categorical_cols = [col for col in CATEGORICAL_COLS if col in input_data.columns]
        input_data = pd.get_dummies(input_data, columns=existing_categorical_cols, drop_first=True)


        # Ensure all expected columns are present
        expected_columns = model.feature_names_in_
        for col in expected_columns:
            if col not in input_data.columns:
                input_data[col] = 0  # Add missing dummy columns with 0

        # Reorder columns to match training
        input_data = input_data[expected_columns]

        # Scale numeric columns
        input_data[NUMERIC_COLS] = scaler.transform(input_data[NUMERIC_COLS])

        # Predict
        prediction = model.predict(input_data)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "prediction": int(prediction[0])
            })
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": str(e)
            })
        }
