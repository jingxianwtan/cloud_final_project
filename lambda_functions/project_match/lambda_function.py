import json
import boto3
import logging
import uuid
import utils
from boto3.dynamodb.conditions import Key, Attr

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    sqs = boto3.client('sqs')
    sns = boto3.client('sns')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/267139716268/match_queue.fifo'
    
    sqs_response = poll_sqs(sqs, queue_url)
    messages = sqs_response['Messages'] if 'Messages' in sqs_response.keys() else []
    logger.info("message is: {}".format(messages))
    
    process_messages(sqs, sns, queue_url, messages)

    return {
        'statusCode': 200,
        'body': "finished"
    }
    

def process_messages(sqs, sns, queue_url, messages):
    dynamodb = boto3.resource('dynamodb')
    notes_table = dynamodb.Table('user_notes')
    user_table = dynamodb.Table('project_user')
    
    for message in messages:
        msg_attributes = message["MessageAttributes"]
        note_user_id = message["Body"]
        note_lad = msg_attributes['lat']['StringValue']
        note_lng = msg_attributes['lng']['StringValue']
        note_date = msg_attributes['date']['StringValue']
        note_category = msg_attributes['category']['StringValue']
        note_id = msg_attributes['note_id']['StringValue']
        
        response = notes_table.scan(
            FilterExpression=Attr('date').eq(note_date) & Attr('category').eq(note_category)
        )
        text = ""
        for item in response['Items']:
            if text == "" and item['note_id'] != note_id and item['user_id'] != note_user_id and utils.calculate_distance(note_lad, note_lng, item['lat'], item['lng']) < 1:
                text = utils.compose_text_message(item['category'], item['location'], item['event'])
                phone = user_table.get_item(Key={'UUID':note_user_id})['Item']['Phone']
                # phone = "9178325536"
                logger.info("Sending text message to: {}".format(phone))
                utils.publish_sns(sns, text, phone)

        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )


def poll_sqs(sqs, queue_url):
    return sqs.receive_message(
        QueueUrl=queue_url,
        MessageAttributeNames=[
            'lat', 'lng', 'date', 'category', 'note_id', 'event'
        ],
        MaxNumberOfMessages=10,
        VisibilityTimeout=10,
        WaitTimeSeconds=20,
        ReceiveRequestAttemptId=str(uuid.uuid1()).replace("-", "")
    )
