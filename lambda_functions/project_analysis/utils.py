import json
from botocore.vendored import requests
import uuid

def google_map_search(location):
    location = location.replace(' ', '+')
    http = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + location + '&key=<Google API Key>'
    response = requests.get(http)
    return response.json()

def convert_time(datetime):
    datetime_array = datetime.split(" ")
    
    for dt in datetime_array:
        dt = dt.lower()
        time = "00:00:00"
        if "am" in dt:
            time = dt.replace("am","")
            if int(time) >= 10:
                time = time + ":00:00"
            else:
                time = "0" + time + ":00:00"
        elif "pm" in dt:
            time_int = int(dt.replace("pm","")) + 12
            time = str(time_int) + ":00:00"
    return time

def check_content(string, location, datetime):
    s_array = string.split(" ")
    for s in s_array:
        if s in location or s in datetime:
            return False
    return True

def send_to_sqs(sqs, note):
    queue_url = 'https://sqs.us-east-1.amazonaws.com/267139716268/match_queue.fifo'
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=note['user_id'],
        MessageAttributes={
            'lat': {
                'StringValue': note['lat'],
                'DataType': 'String'
            },
            'lng': {
                'StringValue': note['lng'],
                'DataType': 'String'
            },
            'date': {
                'StringValue': note['date'],
                'DataType': 'String'
            },
            'category': {
                'StringValue': note['category'],
                'DataType': 'String'
            },
            'note_id': {
                'StringValue': note['note_id'],
                'DataType': 'String'
            },
            'event': {
                'StringValue': note['event'],
                'DataType': 'String'
            }
        },
        MessageDeduplicationId=str(uuid.uuid1()).replace("-", ""),
        MessageGroupId='match_note'
    )
    return response