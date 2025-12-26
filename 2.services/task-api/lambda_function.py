import json
import os
import boto3
import uuid

dynamodb = boto3.resource("dynamodb")
sqs = boto3.client("sqs")

TABLE_NAME = os.environ["TASKS_TABLE"]
QUEUE_URL = os.environ["EVENTS_QUEUE_URL"]

table = dynamodb.Table(TABLE_NAME)

def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        task_id = body.get("taskId") or str(uuid.uuid4())

        item = {
            "taskId": task_id,
            "status": "CREATED"
        }

        table.put_item(Item=item)

        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({
                "eventType": "TASK_CREATED",
                "taskId": task_id
            })
        )

        return response(201, {
            "message": "Task created",
            "taskId": task_id
        })

    except Exception as e:
        return response(500, {"error": str(e)})