# Using AWS to build a demo dining suggestion concierge

## Architecture
See [Description](./CC_Spring24_Assignment1.pdf)

## Components

### S3 
Static Web holding  

### API Gateway 
Defining api interface of frontend's request to lambda_0 and response  

### Lambda function -- LF0
Hanlding request from frontend, send user input to lex, receive lex response and send back  

### Lambda function -- LF1
Validation of lex slots; send message to SQS after fulfillment

### Simple Queue Service
Buffering message from LF1

### Lambda function -- LF2
Poll message from SQS, query on OpenSearch to get recommendation

### DynamoDB
Store restaurants information

### OpenSearch
Sync data with DynamoDB and provide query response

### Lambda function -- ddb-to-opensearch
Use dynamo stream as trigger, sync data to opensearch.