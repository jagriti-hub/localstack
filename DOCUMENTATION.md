Sure, here's an example `DOCUMENTATION.md` file:

# SQS DynamoDB Tool

## Tool introduction/explanation

The SQS DynamoDB Tool is a command-line tool that allows you to consume messages from an AWS SQS queue, store the results in an AWS DynamoDB database, and show the results when asked. The tool is designed to be used with a local development environment, using LocalStack to simulate the AWS services.

## How to build the tool and build requirements

To build the tool, you will need to have Docker and Docker-compose installed on your local machine. The tool is built as a Docker container, which includes all of the necessary dependencies.

## How to configure the environment
If we want to run the tool without docker we need to configure aws with a dummy access and secret key.
But as we are using docker-compose the necessary environment configuration is mentioned in it already. Hence we don't need to configure anythin locally.

## How to run the tool

To run the tool, you need to use the `docker-compose` command. The `docker-compose.yml` file contains the configuration for the Docker container and the environment variables required to run the tool. To start the container, run the following command:

```bash
docker-compose up -d
```

This command will initialize the localstack environment and build the Docker image, create a container, and start the tool inside the container.

## How to use the tool
Before using the tool you can run 
```
aws configure --profile localstack
```
you can provide dunmmy access and secret key and default region as us-east-1 as we are using us-east-1 region in docker-compose setup.

And you can use below command for sending message to the queue name which we are using in docker-compose. we are using my-queue as queue name.

```
python3 sendmessage.py
```

The SQS DynamoDB Tool supports the following options:

- `consume --count n`: Consume `n` messages and print the message content and message IDs from the SQS context.
- `show`: Show all consumed messages and print the message content and message IDs from the SQS context.
- `clear`: Clear all consumed messages from the DynamoDB database.

To use the tool, simply specify one of the options as a command-line argument. For example, to consume 10 messages, run the following command:

```
docker exec -it localstack_sqs-dynamodb-tool_1  python3 sqs-dynamodb-tool.py consume --count 10
```

This will consume 10 messages and print the message content and message IDs.

To show all consumed messages, run the following command:

```
docker exec -it localstack_sqs-dynamodb-tool_1  python3 sqs-dynamodb-tool.py show
```

This will show all consumed messages and print the message content and message IDs.

To clear all consumed messages from the DynamoDB database, run the following command:

```
docker exec -it localstack_sqs-dynamodb-tool_1  python3 sqs-dynamodb-tool.py clear
```

This will clear all consumed messages from the DynamoDB database.

## Challenges Faced

During the development of the command line tool, there were a few challenges that were encountered. 

1. **Setting up localstack and using it in local:** It was initially challenging to set up localstack in docker, especially since it required a lot of configuration to get everything running smoothly. When I tried testing the python script locally i faced and learned the configuration which is required to be done.

2. **Debugging issues:** Debugging issues with the code was also a challenge, especially since there were several components involved. It was important to ensure that messages were being correctly consumed from SQS and that they were being correctly stored in DynamoDB.

2. **Making the tool as a docker tool:** Running the tool using docker command was a challanging part for me as I faced issue with path not found if I was trying to run the docker using CMD or ENTYPOINT as python command. Hence I made the required changes in Dockerfile so that after docker-compose up -d it will stay in running state.

4. **Documentation:** Writing the documentation was also challenging, especially since it was important to ensure that everything was clearly explained and that users could easily understand how to use the tool.

## Conclusion

Despite the challenges, the development of the command line tool was a great learning experience. It provided an opportunity to work with Docker and localstack, which are useful tools for testing and developing AWS applications locally.