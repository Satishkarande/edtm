import json
import os
import boto3
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
sqs = boto3.client("sqs")

TABLE_NAME = os.environ.get("TASKS_TABLE")
QUEUE_URL = os.environ.get("EVENTS_QUEUE_URL")

table = dynamodb.Table(TABLE_NAME)


def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        if "taskId" not in body:
            return response(400, {"error": "taskId is required"})

        item = {
            "taskId": body["taskId"],
            "status": body.get("status", "CREATED"),
            "createdAt": datetime.utcnow().isoformat()
        }

        # 1️⃣ Save task to DynamoDB
        table.put_item(Item=item)

        # 2️⃣ Publish event to SQS
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({
                "eventType": "TASK_CREATED",
                "taskId": body["taskId"]
            })
        )

        return response(201, {
            "message": "Task created",
            "taskId": body["taskId"]
        })
#12S
    except Exception as e:
        print("ERROR:", str(e))
        return response(500, {"error": "Internal Server Error"})