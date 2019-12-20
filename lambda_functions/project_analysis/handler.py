import boto3
import utils
import lex
import json
import uuid
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def analysis_input(intent_request):
    text = intent_request['content']
    comprehend = boto3.client('comprehend')
    
    entities_response = comprehend.detect_entities(
        Text=text,
        LanguageCode='en'
    )
    keyphrase_response = comprehend.detect_key_phrases(
    Text=text,
    LanguageCode='en'
    )
    
    entities = entities_response['Entities']
    keyphrase = keyphrase_response['KeyPhrases']
    datetime = ""
    location = ""
    event = ""
    
    for s in entities:
        if s['Type'] == 'DATE':
            datetime = datetime + " " + s['Text']
        elif s['Type'] == "ORGANIZATION" or "LOCATION" or "PERSON":
            location = location + " " + s['Text']
    
    location = location.strip()
    datetime = datetime.strip()
    
    date_response = lex.query_lex(intent_request['userId'], datetime)
    date = date_response['slots']['Date']
    time = utils.convert_time(datetime)
    
    for k in keyphrase:
        if location in k['Text']:
            location = k['Text']
        elif utils.check_content(k['Text'], location, datetime):
            event = k['Text']
    
    search = utils.google_map_search(location)
    
    if len(search['results']) > 0:
        location_name = search['results'][0]['name']
        location_lat = search['results'][0]['geometry']['location']['lat']
        location_lng = search['results'][0]['geometry']['location']['lng']
        location_add = search['results'][0]['formatted_address']
    else:
        location_name = location
        location_lat = ''
        location_lng = ''
        location_add = ''
    
    result = {}
    result['Event'] = event
    result['Time'] = date + " " + time
    result['Location'] = location_name
    result['Address'] = location_add
    result['Latitude'] = location_lat
    result['Longitude'] = location_lng
    
    cors = {
            "Access-Control-Allow-Origin":"*",
            "Access-Control-Allow-Methods":"GET,POST,OPTIONS",
            "Access-Control-Allow-Headers":"Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Content-Type":"application/json"
        }
    
    return {
                'statusCode': 200,
                'headers': cors,
                'body': json.dumps(result)
            }


def verify_address(intent_request):
    location = intent_request['content']
    
    search = utils.google_map_search(location)
    
    if len(search['results']) > 0:
        location_name = search['results'][0]['name']
        location_lat = search['results'][0]['geometry']['location']['lat']
        location_lng = search['results'][0]['geometry']['location']['lng']
        location_add = search['results'][0]['formatted_address']
    else:
        location_name = location
        location_lat = ''
        location_lng = ''
        location_add = ''
    
    result = {}
    result['Location'] = location_name
    result['Address'] = location_add
    result['Latitude'] = location_lat
    result['Longitude'] = location_lng
    
    cors = {
            "Access-Control-Allow-Origin":"*",
            "Access-Control-Allow-Methods":"GET,POST,OPTIONS",
            "Access-Control-Allow-Headers":"Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Content-Type":"application/json"
        }
    
    return {
                'statusCode': 200,
                'headers': cors,
                'body': json.dumps(result)
            }

def confirm_input(body):
    dynamodb = boto3.resource('dynamodb')
    notes_table = dynamodb.Table('user_notes')
    sqs = boto3.client("sqs")
    
    item = {
            'address': body['Address'],
            'category': body['Category'],
            'date': body['Time'],
            'event': body['Event'],
            'lat': body['Lat'],
            'lng': body['Lng'],
            'location': body['Place'],
            'location_plus': body['Place'].replace(" ","+"),
            'note_id': str(uuid.uuid4()),
            'text': body['Text'],
            'user_id': body['userId']
        }
        
    notes_table.put_item(
        Item = item
    )
    
    res = utils.send_to_sqs(sqs, item)
    logger.debug("Sending result {} to queue...".format(res))
    
    cors = {
            "Access-Control-Allow-Origin":"*",
            "Access-Control-Allow-Methods":"GET,POST,OPTIONS",
            "Access-Control-Allow-Headers":"Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Content-Type":"application/json"
        }
    
    return {
                'statusCode': 200,
                'headers': cors,
                'body': json.dumps('s')
            }
    

    
