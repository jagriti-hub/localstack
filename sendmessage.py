import boto3

sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')

queue_url  = sqs.create_queue(QueueName='my-queue')['QueueUrl']

message = "Hello, world!"
response = sqs.send_message(QueueUrl=queue_url, MessageBody=message)
print(f"Message sent with ID: {response['MessageId']}")