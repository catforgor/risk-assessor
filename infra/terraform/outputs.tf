output "transactions_queue_url" {
  value = aws_sqs_queue.transactions.url
}

output "transactions_queue_arn" {
  value = aws_sqs_queue.transactions.arn
}
