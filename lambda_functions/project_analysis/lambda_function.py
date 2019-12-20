import json
import os, time
import handlers
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    logger.info("event is: {}".format(event))

    os.environ['TZ'] = 'America/New_York'
    time.tzset()

    
    
    # text = 'I want to study for final exam at Bobst library this weekend.'
    # text = 'I want to study at Dibner library this Sunday.'
    
    request = json.loads(event['body'])

    logger.info('request is {}'.format(request))
    
    flag = request['flag']
    
    if flag == "full":
        return handlers.analysis_input(request)
    elif flag == "final":
        return handlers.confirm_input(request)
    elif flag == "place":
        return handlers.verify_address(request)
