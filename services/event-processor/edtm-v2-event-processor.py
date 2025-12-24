import json
import boto3

ssm = boto3.client('ssm')
sfn = boto3.client('stepfunctions')

def get_param(name):
    return ssm.get_parameter(Name=name)['Parameter']['Value']

WORKFLOW_ARN = get_param('/edtm-v2/workflow_arn')

def lambda_handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])

        # Loop guard: process only known events
        if body.get("eventType") != "TASK_CREATED":
            print("Ignoring event:", body)
            continue
        #log line for CICD Pipe line test

        sfn.start_execution(
            stateMachineArn=WORKFLOW_ARN,
            input=json.dumps({
                "taskId": body["taskId"],
                "source": "edtm-v2"
            })
        )
#1234S
        print("Workflow started for task:", body["taskId"])
