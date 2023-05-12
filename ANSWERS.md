## ANSWERS

### Q1: Please explain what is the advantage of using SQS in this solution.

The advantage of using SQS (Simple Queue Service) in this solution is that it provides a reliable, scalable, and fully managed messaging service that can decouple the components of a cloud application. With SQS, we can decouple the producer and the consumer of messages, which means that the producer doesn't have to wait for the consumer to process the message before sending the next message. This leads to increased application performance and scalability. Additionally, SQS ensures that each message is processed only once, so we can avoid message duplication and potential race conditions.

### Q2: Compare SQS to a message broker you have used before. What are the differences? Strong/weak points? (If you did not use such a solution, please skip this question)

I have used Kafka as a message broker before, and there are several differences between Kafka and SQS. Kafka is a distributed streaming platform that can process high volumes of data in real-time, while SQS is a fully managed messaging service that focuses on reliably delivering messages between producers and consumers. One of the strengths of Kafka is its ability to store and process large amounts of data in real-time, making it suitable for use cases that require low latency and high throughput. However, Kafka can be complex to set up and manage, and it requires more infrastructure resources compared to SQS. On the other hand, SQS is easy to use and manage, and it is suitable for use cases where reliability and scalability are important.

### Q3: If we run multiple instances of this tool, what prevents a message from being processed twice?

To prevent a message from being processed twice when running multiple instances of this tool, we can use SQS's visibility timeout feature. When a message is received by a consumer, it becomes invisible to other consumers for a period of time defined by the visibility timeout. During this time, the consumer processes the message and then deletes it from the queue. If the consumer fails to process the message within the visibility timeout period, the message becomes visible again, and another consumer can pick it up. This ensures that each message is processed only once, even when running multiple instances of the tool.

### Q4: In very rough terms, can you suggest an alternative solution aside from using SQS from your previous experience using different technologies?

One alternative solution that I have used before is Kafka. I have explained the pros and cons in Q2.