import json

import boto3

from decimal import Decimal

from datetime import datetime

dynamodb = boto3.resource('dynamodb')

def handle_decimal_type(obj):
    if isinstance(obj, Decimal):
        if float(obj).is_integer():
            return int(obj)
        else:
            return float(obj)
    raise TypeError

def get_todo(event, context):
    table = dynamodb.Table('Todos')

    response = table.scan()

    print(response)

    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return {
        "statusCode": 200,
        "body": json.dumps(data, default=handle_decimal_type),
        "headers": {
            "Content-Type": "text/json"
        }
    }


def post_todo(event, context):
    table = dynamodb.Table('Todos')

    print(event)

    json_object = json.loads(event['body'])

    now = datetime.now()

    now_string = now.strftime("%Y/%m/%d %H:%M:%S")

    response = table.put_item(
        Item={
            'title': json_object['title'],
            'description': json_object['description'],
            'create_time': now_string,
            'completed': 0
        })

    print(response)

    return {
        "statusCode": 200,
        "body": "{\"success\": \"true\"}",
        "headers": {
            "Content-Type": "text/json"
        }
    }

def put_todo(event, context):
    table = dynamodb.Table('Todos')

    json_object = json.loads(event['body'])

    response = table.update_item(
        Key={'title': json_object['title']},
        UpdateExpression="set completed = :g",
        ExpressionAttributeValues={
            ':g': 1
        },
        ReturnValues="UPDATED_NEW"
    )

    print(response)

    return {
        "statusCode": 200,
        "body": "{\"success\": \"true\"}",
        "headers": {
            "Content-Type": "text/json"
        }
    }
