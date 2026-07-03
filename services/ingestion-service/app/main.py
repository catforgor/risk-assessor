import os

import boto3
from fastapi import FastAPI

from .schemas import Transaction

app = FastAPI(title="ingestion-service")


def get_sqs_client():
    return boto3.client("sqs", region_name=os.environ.get("AWS_REGION", "eu-west-1"))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/transactions", status_code=201)
def submit_transaction(transaction: Transaction):
    queue_url = os.environ["TRANSACTIONS_QUEUE_URL"]
    sqs = get_sqs_client()
    sqs.send_message(QueueUrl=queue_url, MessageBody=transaction.model_dump_json())
    return transaction
