import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def retrieve_notes(event):

    dynamodb = boto3.resource('dynamodb')
    notes_table = dynamodb.Table('user_notes')
    user_table = dynamodb.Table('project_user')
    
    now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    
    note_items = notes_table.scan(
        FilterExpression=Attr('date').gt(now)
    )
    logger.info("note returned: {}".format(note_items))
    
    return {
        'Items': beautify_notes(user_table, note_items)
        }


def contact_poster(event):
    sns = boto3.client('sns')
    dynamodb = boto3.resource('dynamodb')
    notes_table = dynamodb.Table('user_notes')
    user_table = dynamodb.Table('project_user')
    
    note_id = event['note_id']
    sortKey = event['category']
    user_id = event['user_id']
    
    response = notes_table.get_item(Key={'note_id':note_id, 'category':sortKey})
    poster_id = response['Item']['user_id']
    poster_item = user_table.get_item(Key={'UUID':poster_id})
    poster_phone = poster_item['Item']['Phone']
    event = response['Item']['event']
    location = response['Item']['location']
    
    requester = user_table.get_item(Key={'UUID':user_id})
    requester_name = requester['Item']['Username']
    requester_phone = requester['Item']['Phone']
    
    text = requester_name + " is interested at your event " + event + " at " + location + ", his phone number is " + requester_phone
    sns_response = publish_sns(sns, text, poster_phone)
    return {
                'statusCode': 200,
                'body': json.dumps(sns_response)
            }


def publish_sns(sns, text, phone):
    print(phone)
    return sns.publish(
        PhoneNumber="+1" + phone,
        Message=text,
        MessageAttributes={
            'AWS.SNS.SMS.SenderID': {
                'DataType': 'String',
                'StringValue': 'image'
            },
            'AWS.SNS.SMS.SMSType': {
                'DataType': 'String',
                'StringValue': 'Transactional'
            }
        }
    )
    
def delete_notes(event):

    dynamodb = boto3.resource('dynamodb')
    notes_table = dynamodb.Table('user_notes')
    
    notes_table.delete_item(
    Key={
        'note_id': event['note_id'],
        'category': event['category']
    }
    )
    return


def beautify_notes(user_table, note_items):
    notes = []
    for item in note_items['Items']:
        user_item = user_table.get_item(Key={'UUID':item['user_id']})
        item['username'] = user_item['Item']['Username']
        notes.append(item)
        logger.info("item is {}".format(item))
    return notes
