import json
import os
import boto3

sfn = boto3.client("stepfunctions")

WORKFLOW_ARN = os.environ["WORKFLOW_ARN"]

def lambda_handler(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])

        if body.get("eventType") != "TASK_CREATED":
            continue

        sfn.start_execution(
            stateMachineArn=WORKFLOW_ARN,
            input=json.dumps({
                "taskID": body["taskID"]
            })
        )