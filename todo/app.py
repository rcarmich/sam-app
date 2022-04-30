import json

import boto3

from decimal import Decimal

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

    now = datetime.now()

    now_string = now.strftime("%Y/%m/%d %H:%M:%S")

    response = table.put_item(
        Item={
            'title': event['title'],
            'description': event['description'],
            'create_time': now_string,
            'completed': 0
        })

    print(response)

    return {
        "statusCode": 200
    }

def put_todo(event, context):
    table = dynamodb.Table('Todos')

    response = table.update_item(
        Key={'title': event['title']},
        AttributeUpdates={
            'completed': 1
        }
    )

    print(response)

    return {
        "statusCode": 200
    }
