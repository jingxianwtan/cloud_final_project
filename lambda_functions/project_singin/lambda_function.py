from DynamoDBService import DynamoDBService
import boto3
import botocore
import json

def lambda_handler(event, context):
    # TODO implement
    myBody = json.loads(event['body'])
    myPhone = myBody['phone']
    myPassword = myBody['password']
    dynamodb = DynamoDBService()
    result = dynamodb.operate_table(phone = myPhone, password = myPassword)
    body = ''
    code = 200
    cors = {
        "Access-Control-Allow-Origin":"*",
        "Access-Control-Allow-Methods":"GET,OPTIONS",
        "Access-Control-Allow-Headers":"Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Content-Type":"application/json"
    }
    if result:
        body = dynamodb.get_UID(phone = myPhone, password = myPassword)
    else:
        body = 'fail'
        code = 502
    return {
        'statusCode': code,
        'body': body,
        'headers': cors
    }
