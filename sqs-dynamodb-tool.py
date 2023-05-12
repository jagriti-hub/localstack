import argparse
import boto3
import os
from botocore.exceptions import ClientError

# AWS service endpoints
ENDPOINT_URL = os.environ['ENDPOINT_URL']

# Set up SQS and DynamoDB clients
sqs_client = boto3.client('sqs', endpoint_url=ENDPOINT_URL)
dynamodb_client = boto3.client('dynamodb', endpoint_url=ENDPOINT_URL)

# Set up SQS and DynamoDB resource
sqs = boto3.resource('sqs', endpoint_url=ENDPOINT_URL)
dynamodb = boto3.resource('dynamodb', endpoint_url=ENDPOINT_URL)

# Initialize DynamoDB table
table_name = os.environ['TABLE_NAME']
try:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        BillingMode='PAY_PER_REQUEST'
    )
except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceInUseException':
        pass
    else:
        raise


# Initialize SQS queue
queue_name = os.environ['QUEUE_NAME']
queue_url = sqs_client.create_queue(QueueName=queue_name)['QueueUrl']

# Define command line arguments
parser = argparse.ArgumentParser(description='Consume messages from SQS and store results in DynamoDB')
subparsers = parser.add_subparsers(dest='command')

consume_parser = subparsers.add_parser('consume', help='Consume n messages from SQS and store results in DynamoDB')
consume_parser.add_argument('--count', type=int, required=True, help='Number of messages to consume')

show_parser = subparsers.add_parser('show', help='Show all consumed messages from DynamoDB')

clear_parser = subparsers.add_parser('clear', help='Clear all consumed messages from DynamoDB')

def process_message(message):
    # Parse the message and return the result as a dictionary
    return {
        'id': message['MessageId'],
        'data': message['Body']
    }

# Define functions for each subcommand
def consume(args):
    count = args.count
    while True:
        messages = sqs_client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=count, VisibilityTimeout=15)
        if 'Messages' not in messages:
            break
        message_list=[]
        for message in messages['Messages']:
            result = process_message(message)
            if result['data'] not in message_list:
                message_list.append(message['Body'])
                dynamodb_client.put_item(
                    TableName=table_name,
                    Item={
                        'id': {'S': result['id']},
                        'data': {'S': result['data']}
                    }
                )
                print(f"Received message: {message['Body']}")
            sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])

def show(args):
    show_table = dynamodb.Table(table_name)
    response = show_table.scan()
    messages = response['Items']
    while 'LastEvaluatedKey' in response:
        response = show_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        messages.extend(response['Items'])

    for message in messages:
        print(message)

def clear(args):
    table = dynamodb.Table(table_name)
    response = table.scan()
    with table.batch_writer() as batch:
        for message in response['Items']:
            batch.delete_item(Key={'id': message['id']})
    print('Deleted all messages from DynamoDB table')

# Parse command line arguments and execute subcommand
args = parser.parse_args()
if args.command == 'consume':
    consume(args)
elif args.command == 'show':
    show(args)
elif args.command == 'clear':
    clear(args)
else:
    parser.print_help()
