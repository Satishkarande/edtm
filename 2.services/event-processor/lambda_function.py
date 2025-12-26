import json
import os
import boto3

ssm = boto3.client("ssm")
sfn = boto3.client("stepfunctions")

def get_param(name):
    return ssm.get_parameter(Name=name)["Parameter"]["Value"]

WORKFLOW_ARN = get_param("/edtm/workflow_arn")

def lambda_handler(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])

        if body.get("eventType") != "TASK_CREATED":
            print("Ignoring event:", body)
            continue

        sfn.start_execution(
            stateMachineArn=WORKFLOW_ARN,
            input=json.dumps({
                "taskID": body["taskID"],
                "source": "edtm"
            })
        )

        print("Started workflow for", body["taskID"])