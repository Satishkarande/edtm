import json, os, boto3
ssm = boto3.client('ssm')
ddb = boto3.client('dynamodb')
sqs = boto3.client('sqs')

def get_param(name):
    return ssm.get_parameter(Name=name)['Parameter']['Value']

TASKS_TABLE = get_param('/edtm-v2/tasks_table')
EVENTS_QUEUE_URL = get_param('/edtm-v2/events_queue_url')

def response(code, body):
    return {"statusCode": code, "headers": {"Content-Type": "application/json"}, "body": json.dumps(body)}

def lambda_handler(event, context):
    method = event.get('requestContext', {}).get('http', {}).get('method')
    if method == 'POST':
        body = json.loads(event['body'])

        # 1) Save task (sync)
        ddb.put_item(
            TableName=TASKS_TABLE,
            Item={
                "taskId": {"S": body["taskId"]},
                "title": {"S": body.get("title","")},
                "status": {"S": body.get("status","CREATED")}
            }
        )

        # 2) Publish event (async)
        sqs.send_message(
            QueueUrl=EVENTS_QUEUE_URL,
            MessageBody=json.dumps({
                "eventType": "TASK_CREATED",
                "taskId": body["taskId"]
            })
        )

        return response(201, {"message":"Task created"})

    return response(400, {"error":"Unsupported"})