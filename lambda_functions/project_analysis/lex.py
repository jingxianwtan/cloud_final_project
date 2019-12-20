import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def query_lex(user_id, date):
    client = boto3.client('lex-runtime')
    response = client.post_text(
        botName='datetime_bot',
        botAlias='$LATEST',
        userId=user_id,
        sessionAttributes={},
        requestAttributes={},
        inputText='the day is ' + date
    )
    logger.debug(response)

    return response
