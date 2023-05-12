FROM python:3.9

WORKDIR /app

COPY . .

RUN chmod +x sqs-dynamodb-tool.py

RUN pip install -r requirements.txt

# ENTRYPOINT [ "/bin/bash" ]
CMD tail -f /dev/null