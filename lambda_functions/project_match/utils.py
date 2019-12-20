import datetime
from math import sin, cos, sqrt, atan2, radians
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def calculate_distance(lat1, lng1, lat2, lng2):
    
    logger.info("calculating distance")
    
    R = 6373.0
    lat1 = radians(float(lat1))
    lng1 = radians(float(lng1))
    lat2 = radians(float(lat2))
    lng2 = radians(float(lng2))
    
    dlon = lng2 - lng1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    logger.info("distance is " + str(distance))
    return distance

def compose_text_message(category, location, event):
    return 'we found an event \"' + event + '\" for category \"' + category + '\" near by at ' + location + ' that you might be interested at. If you are, please go to the note page to contact.'

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
