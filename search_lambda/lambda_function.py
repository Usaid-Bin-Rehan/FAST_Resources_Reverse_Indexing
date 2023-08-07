import boto3
import json
from boto3.dynamodb.conditions import Key

print('Loading function')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FAST-Resources_Search')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Allow-Methods': "*",
            'Access-Control-Allow-Headers': 'Content-Type, Access-Control-Allow-Origin'
        },
    }


def query_dynamo_db(keyword):
    okay = table.query(
        KeyConditionExpression=Key('pk').eq(keyword)
    )
    rows = {item['file_path']: item for item in okay['Items']}
    for key, value in rows.items():
        del value['pk']
        del value['file_path']
    return rows


def intersect_result_v2(results):
    if len(results) == 1:
        return results[0]

    intersect = results[0]
    for i in range(1, len(results)):
        intersect = {x: intersect[x] for x in intersect if x in results[i]}

    return intersect


def intersect_result(results):
    if len(results) == 1:
        return list(results[0].keys())

    intersect = results[0]
    for i in range(1, len(results)):
        intersect = {x: intersect[x] for x in intersect if x in results[i]}

    return list(intersect.keys())


def lambda_handler(event, context):
    operations = {
        'GET': lambda dynamo, x: dynamo.scan(**x),
    }
    operation = event['httpMethod']
    if operation in operations:
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        print(event)

        query_words = [individual_word.strip() for individual_word in payload['query'].lower().split(' ')]
        results = [query_dynamo_db(word) for word in query_words]

        if event["requestContext"]["stage"] == 'v2':
            return respond(None, intersect_result_v2(results))
        return respond(None, intersect_result(results))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
