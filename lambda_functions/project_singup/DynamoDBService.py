import boto3
from boto3 import Session
from boto3.dynamodb.conditions import Attr, Key
import json
import uuid
 
 
class DynamoDBService:
    def __init__(self):
        pass
 
    def get_service(self, table_name):
        client = boto3.client('dynamodb')
        dynamodb = boto3.resource('dynamodb')
        table_handle = dynamodb.Table(table_name)
        return table_handle
 
    def operate_table(self,phone, name, gender, password, table_name="project_user"):
        table_handle_h5_visit_info = self.get_service(table_name)
        response = table_handle_h5_visit_info.scan(
            FilterExpression=Attr('Phone').eq(phone)
        )
        if response['Items'] != []:
            return False
        uid = str(uuid.uuid4())
        table_handle_h5_visit_info.put_item(
            Item = {
                "UUID": uid,
                "Phone": phone,
                "Username": name,
                "Gender": gender,
                "Password": password
            }
        )

        return True