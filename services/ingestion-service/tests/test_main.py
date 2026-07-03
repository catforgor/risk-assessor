import boto3
import pytest
from fastapi.testclient import TestClient
from moto import mock_aws

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.fixture
def transactions_queue_url(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_REGION", "eu-west-1")
    with mock_aws():
        sqs = boto3.client("sqs", region_name="eu-west-1")
        queue_url = sqs.create_queue(QueueName="test-transactions")["QueueUrl"]
        monkeypatch.setenv("TRANSACTIONS_QUEUE_URL", queue_url)
        yield sqs, queue_url


def test_submit_transaction_publishes_to_queue(transactions_queue_url):
    sqs, queue_url = transactions_queue_url
    payload = {
        "transaction_id": "tx_1",
        "account_id": "acc_1",
        "amount": 42.50,
        "currency": "GBP",
        "timestamp": "2026-07-02T12:00:00Z",
        "merchant": "Tesco",
    }

    response = client.post("/transactions", json=payload)

    assert response.status_code == 201
    assert response.json()["transaction_id"] == "tx_1"

    messages = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
    assert len(messages.get("Messages", [])) == 1


def test_submit_transaction_rejects_non_positive_amount(transactions_queue_url):
    payload = {
        "transaction_id": "tx_2",
        "account_id": "acc_1",
        "amount": 0,
        "currency": "GBP",
        "timestamp": "2026-07-02T12:00:00Z",
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 422
