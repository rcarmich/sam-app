import json

import boto3

def post_todo(event, context):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Todos')

    response = table.put_item(
        Item={
            'title': 'Walk the dog',
            'description': 'Take the dog for a walk, she needs the exercise',
            'create_time': 'April 10, 2022 02:00 PM',
            'completed': 0
        })

    print(response)

    return {
        "statusCode": 200
    }

def put_todo(event, context):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Todos')

    response = table.put_item(
        Item={
            'title': 'Walk the dog',
            'description': 'Take the dog for a walk, she needs the exercise',
            'create_time': 'April 10, 2022 02:00 PM',
            'completed': 0
        })

    pprint(response, sort_dicts=False)

    return {
        "statusCode": 200
    }
