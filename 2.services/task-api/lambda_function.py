import json
import os
import boto3

dynamodb = boto3.resource("dynamodb")
sqs = boto3.client("sqs")

TABLE_NAME = os.environ["TASKS_TABLE"]
QUEUE_URL = os.environ["EVENTS_QUEUE_URL"]

table = dynamodb.Table(TABLE_NAME)

def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        if "taskID" not in body:
            return response(400, {"error": "taskID is required"})

        task_id = body["taskID"]

        # 1️⃣ Write to DynamoDB
        table.put_item(
            Item={
                "taskID": task_id,
                "status": "CREATED"
            }
        )

        # 2️⃣ Send event to SQS
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({
                "eventType": "TASK_CREATED",
                "taskID": task_id
            })
        )

        return response(201, {
            "message": "Task created",
            "taskID": task_id
        })

    except Exception as e:
        print("ERROR:", str(e))
        return response(500, {"error": "Internal Server Error"})