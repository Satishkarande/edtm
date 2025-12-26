import json
import os
import boto3

stepfunctions = boto3.client("stepfunctions")

STATE_MACHINE_ARN = os.environ.get("WORKFLOW_ARN")


def lambda_handler(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])

        # Safety check (prevents loops)
        if body.get("eventType") != "TASK_CREATED":
            print("Ignoring event:", body)
            continue

        task_id = body["taskId"]

        # Start Step Function workflow
        stepfunctions.start_execution(
            stateMachineArn=STATE_MACHINE_ARN,
            input=json.dumps({
                "taskId": task_id,
                "source": "edtm-backend"
            })
        )
#12
        print(f"Workflow started for task {task_id}")