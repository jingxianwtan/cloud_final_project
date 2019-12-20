from DynamoDBService import DynamoDBService
import boto3
import botocore
import json

def lambda_handler(event, context):
    # TODO implement
    myBody = json.loads(event['body'])
    myName = myBody['username']
    myPassword = myBody['password']
    myPhone = myBody['phone']
    myGender = myBody['gender']
    dynamodb = boto3.resource('dynamodb', region_name = "us-east-1", endpoint_url = "https://dynamodb-fips.us-east-1.amazonaws.com")
    table = dynamodb.Table('project_user')
    dynamodbService = DynamoDBService()

    res = dynamodbService.operate_table(myPhone, myName,myGender, myPassword)


   
    cors = {
        "Access-Control-Allow-Origin":"*",
        "Access-Control-Allow-Methods":"POST,OPTIONS",
        "Access-Control-Allow-Headers":"Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Content-Type":"application/json"
    }
    body = ''
    code = ''
    if res:
        body = "success"
        code = 200
    else:
        body = 'email already exist!'
        code = 502
    return {
        'statusCode': code,
        'body': body,
        'headers': cors
    }