import sqlite3
import boto3
from boto3.dynamodb.conditions import Key

## Discontinued, We are now using DynamoDB Import from S3


conn = sqlite3.connect('/Users/jazib/Desktop/workrepo/FAST_Resources_Reverse_Indexer/fast_zakhira.db')
query = """
       SELECT * FROM reverse_index;
       """

# client = boto3.client('dynamodb', region_name="eu-west-1", profile_name="AdministratorAccess-816859564208")
boto3.setup_default_session(profile_name='AdministratorAccess-816859564208')
dynamodb = boto3.resource('dynamodb', region_name="eu-west-1")
table = dynamodb.Table('FAST-Resources_Reverse_Indexer')

okay = table.query(
    KeyConditionExpression=Key('pk').eq('database')
)

print(okay)
cursor = conn.execute(query)

for row in cursor:
    table.put_item(
        Item={
            'pk': row[0],
            'sk': str(row[3]),
            'topic_name': row[1],
            'file_name': row[2],
        }
    )
print('done')
