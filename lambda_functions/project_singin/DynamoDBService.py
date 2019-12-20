import boto3
from boto3 import Session
from boto3.dynamodb.conditions import Attr, Key
import decimal
import json
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)
class DynamoDBService:
    def __init__(self):
        pass
    
 
    def get_service(self, table_name):
        client = boto3.client('dynamodb')
        dynamodb = boto3.resource('dynamodb')
        table_handle = dynamodb.Table(table_name)
        return table_handle
 
    def operate_table(self, phone, password, table_name="project_user"):
        table_handle_h5_visit_info = self.get_service(table_name)
        response = table_handle_h5_visit_info.scan(
            FilterExpression=Attr('Phone').eq(phone)
        )
        items = response['Items'][0]
        return items['Password'] == password
    
    def get_UID(self, phone, password, table_name="project_user"):
        table_handle_h5_visit_info = self.get_service(table_name)
        response = table_handle_h5_visit_info.scan(
            FilterExpression=Attr('Phone').eq(phone)
        )
        items = response['Items'][0]
        return items['UUID']