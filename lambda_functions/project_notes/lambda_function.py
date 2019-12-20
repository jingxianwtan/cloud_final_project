import json
import os, time
import handlers
import logging
import handlers

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    # TODO implement
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }
    
    logger.info("event is: {}".format(event))
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    
    flag = event['flag']
    
    if flag == "notes":
        return handlers.retrieve_notes(event)
    elif flag == "contact":
        return handlers.contact_poster(event)
    elif flag == "delete":
        return handlers.delete_notes(event)
    