import json
import boto3
from datetime import datetime

lex_client = boto3.client("lexv2-runtime", region_name="us-east-1")


def lambda_handler(event, context):

    user_id = (
        "user-id"  # A unique identifier for the user, can be customized as needed.
    )

    messages = event["messages"]
    responses = []

    if messages:

        for message in messages:
            # Define parameters for Lex
            params = {
                "botId": "YourBotId",
                "botAliasId": "YourBotAliasId",
                "localeId": "YourLocaleId",  # e.g., 'en_US'
                "sessionId": user_id,
                "text": message["unstructured"]["text"],
            }

            try:
                lex_response = lex_client.recognize_text(**params)
                response_message = (
                    lex_response["messages"][0]["content"]
                    if lex_response.get("messages")
                    else "No response from Lex."
                )
                responses.append(
                    {
                        "type": "unstructured",
                        "unstructured": {
                            "id": "test-id",
                            "text": response_message,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        },
                    }
                )
            except:
                return {
                    "statusCode": 500,
                    "body": json.dumps({"message": "Error processing Lex response"}),
                }
        return {
            "statusCode": 200,
            "messages": responses,
        }
    else:
        return {"statusCode": 400}
