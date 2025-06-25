Setup for AWS
-----------------
1. Trigger CI/CD pipeline for fraud_detection_lambda/train_model/train.py 
2. Used Lamdha Handler for trigger the event


Sample Dataset to Test after model deployed in s3
----------------------------------------------------

response - 0 = not fraud, 1 = fraud

using curl:
------------

curl -X POST https://your-api-gateway-url.amazonaws.com/prod/predict \
  -H "Content-Type: application/json" \
  -d '{
    "body": "{\"transaction_id\": \"T000204\", \"timestamp\": \"2025-05-23 00:46:48\", \"amount\": 357.2, \"card_type\": \"Visa\", \"merchant_id\": \"M571\", \"merchant_category\": \"food\", \"transaction_type\": \"atm\", \"device_type\": \"mobile\", \"entry_method\": \"chip\", \"customer_id\": \"C5237\", \"customer_age\": 25, \"customer_region\": \"West\", \"is_foreign_transaction\": 0, \"is_high_risk_country\": 0, \"is_weekend\": 0, \"hour_of_day\": 0, \"num_prev_transactions_24h\": 9, \"avg_transaction_amt_24h\": 135.27, \"is_new_device\": 0}"
  }'


using postman:
---------------
URL - https://your-api-gateway-url.amazonaws.com/prod/predict
Request type - POST

{
    "body": {
    "transaction_id": "T000204",
    "timestamp": "2025-05-23 00:46:48",
    "amount": 357.2,
    "card_type": "Visa",
    "merchant_id": "M571",
    "merchant_category": "food",
    "transaction_type": "atm",
    "device_type": "mobile",
    "entry_method": "chip",
    "customer_id": "C5237",
    "customer_age": 25,
    "customer_region": "West",
    "is_foreign_transaction": 0,
    "is_high_risk_country": 0,
    "is_weekend": 0,
    "hour_of_day": 0,
    "num_prev_transactions_24h": 9,
    "avg_transaction_amt_24h": 135.27,
    "is_new_device": 0
    }
}