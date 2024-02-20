import os
from datetime import datetime
import json
import boto3
from botocore.exceptions import ClientError
import requests
from random import randint

SQS_URL = os.environ["sqs"]
OPEN_SEARCH_URL = os.environ["open_search"]
INDEX = os.environ["os_index"]
OS_USER = os.environ["os_user"]
OS_PWD = os.environ["os_pwd"]
TABLE = os.environ["ddb_table"]
SENDER = os.environ["email_sender"]
AWS_REGION = os.environ["aws_region"]


def poll_sqs(event):
    """
    Poll message from SQS, process the message and get required cuisine
    return the requirements(cuisine, email, num_people, time, date, location)
    along with the message id

    ret: queries: list[dict{'query':dict, 'receipt_handle':string}]
    """
    print("POLLING MESSAGE from {} at {}...".format(SQS_URL, event["time"]))
    sqs_client = boto3.client("sqs")
    kwargs = {"QueueUrl": SQS_URL, "MaxNumberOfMessages": 1}
    try:
        response = sqs_client.receive_message(**kwargs)
        print("GOOD RESPONSE from sqs:")
        print(response)
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            messages = response.get("Messages", None)
            if messages is not None:
                queries = []
                for message in messages:
                    body = json.loads(message["Body"])
                    queries.append({"query": body, "receipt_handle": message["ReceiptHandle"]})
                return queries
            else:
                print("NOTHING From SQS!")
                return None
        else:
            print("BAD RESPONSE!")
            print(response)
            return None
    except:
        print("ERROR FROM OPENSEARCH!")
        return None


def open_search_query(queries):
    """
    param:
        queries: list[dict{'query':dict, 'receipt_handle':string}]

    """
    headers = {"Content-Type": "application/json"}
    for query in queries:
        body = {
            "query": {
                "match": {
                    "categories": {
                        "query": f"{query['query']['Cuisine']}",
                        "minimum_should_match": "0",
                    }
                }
            }
        }
        response = requests.get(
            url=f"{OPEN_SEARCH_URL}/{INDEX}/_search",
            auth=(OS_USER, OS_PWD),
            headers=headers,
            data=json.dumps(body),
        )
        if response.status_code == 200:
            print("SUCCESS QUERY")
            message = response.json()
            hits = message["hits"]["hits"]
            if len(hits) > 0:
                recommendation_count = 3 if len(hits) > 3 else len(hits)
                recommendation_index = []
                for i in range(recommendation_count):
                    index = randint(0, len(hits) - 1)
                    if index not in recommendation_index:
                        recommendation_index.append(index)
                recommendation = [hits[i]["_id"] for i in recommendation_index]
                print(f"RECOMMENDATION for {query['receipt_handle']}:")
                print(recommendation)
                query["recommendation"] = recommendation
            else:
                print(f"NO MATCH for {query['receipt_handle']}!")
        else:
            print(f"ERROR QUERY for {query['receipt_handle']}:")
            print(json.dumps(response.json()))
    return queries


def fetch_ddb(queries):
    ddb_client = boto3.client("dynamodb")
    for query in queries:
        results = []
        for id in query["recommendation"]:
            try:
                response = ddb_client.get_item(TableName=TABLE, Key={"id": {"S": id}})
                if (
                    response["ResponseMetadata"]["HTTPStatusCode"] == 200
                    and response["Item"]
                ):
                    item = response["Item"]
                    result = {"name": item["name"]["S"]}
                    if item.get("address", None):
                        result["address"] = [line["S"] for line in item["address"]["L"]]
                    results.append(result)
                else:
                    print(f"NO ITEM {id} in Dynamodb")
            except:
                print("DynamoDB wrong query!")
        query["results"] = results
    return queries


def construct_email(queries):
    for query in queries:
        content = "Hi!\n\nHere are my suggestions on {Cuisine} restaurants for {NumberOfPeople} on {Time} {Date}:\n".format(
            Cuisine=query["query"]["Cuisine"],
            NumberOfPeople=query["query"]["NumberOfPeople"],
            Time=query["query"]["Time"],
            Date=query["query"]["Date"],
        )
        index = 1
        for result in query["results"]:
            name = result["name"]
            address = ", ".join(result["address"])
            detail = "\n{index}. {name}, located at {address}".format(
                index=index, name=name, address=address
            )
            content += detail
            index += 1
        content += "\n\nHope you enjoy your meal!\n\nBest Regards,\nYour Dining Concierge"
        query["email_content"] = content
    return queries


def send_emails(queries):
    # CONFIGURATION_SET = "ConfigSet"
    SUBJECT = "Restaurant Recommendation"
    CHARSET = "UTF-8"
    ses_client = boto3.client("ses", region_name=AWS_REGION)
    sqs_client = boto3.client("sqs")
    for query in queries:
        RECIPIENT = query["query"]["Email"]
        BODY_TEXT = query["email_content"]
        try:
            # Provide the contents of the email.
            response = ses_client.send_email(
                Destination={
                    "ToAddresses": [
                        RECIPIENT,
                    ],
                },
                Message={
                    "Body": {
                        "Text": {
                            "Charset": CHARSET,
                            "Data": BODY_TEXT,
                        },
                    },
                    "Subject": {
                        "Charset": CHARSET,
                        "Data": SUBJECT,
                    },
                },
                Source=SENDER,
            )
            print(response)
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            print(f"Email sent! Message ID: {response['MessageId']}")
            receipt_handle = query['receipt_handle']
            try:
                delete_response = sqs_client.delete_message(QueueUrl=SQS_URL, ReceiptHandle=receipt_handle)
            except:
                print(f"ERROR DELETING sqs message {receipt_handle}")
            else:
                print("SUCCESSFULLY handle one query!")
                print("delete_response")



def lambda_handler(event, context):
    quries = poll_sqs(event=event)
    if quries:
        print("EXTRACTED QUERIES:")
        print(quries)
        quries = open_search_query(queries=quries)
        print("FINISH recommendation：")
        print(quries)
        queries = fetch_ddb(queries=quries)
        print("FINISH data fetching from ddb")
        print(queries)
        queries = construct_email(queries=queries)
        print("FINISH EMAIL construction")
        print(queries)
        print("CHECK COMPLETE at {}".format(str(datetime.now())))
        send_emails(queries=queries)
    else:
        print("FAILED polling messages!")
