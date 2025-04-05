import boto3
import os
from dotenv import load_dotenv
import time

load_dotenv()
AWS_REGION = os.getenv("AWS_REGION")
DYNAMODB_TABLE_NAME = "health_report_conversations"

dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

def store_initial_response(session_id, file_names, model_response):
    timestamp = int(time.time())
    table.put_item(
        Item={
            'session_id': session_id,
            'timestamp': timestamp,
            'role': 'model',
            'content': model_response,
            'file_names': file_names
        }
    )

def store_user_query(session_id, query):
    timestamp = int(time.time())
    table.put_item(
        Item={
            'session_id': session_id,
            'timestamp': timestamp,
            'role': 'user',
            'content': query
        }
    )

def store_model_response(session_id, response):
    timestamp = int(time.time())
    table.put_item(
        Item={
            'session_id': session_id,
            'timestamp': timestamp,
            'role': 'model',
            'content': response
        }
    )

def get_conversation_history(session_id):
    response = table.query(
        KeyConditionExpression='session_id = :sid',
        ExpressionAttributeValues={
            ':sid': session_id
        },
        ScanIndexForward=True
    )
    return response.get('Items', [])

if __name__ == '__main__':
    session = "test_session_123"
    files = ["report1.pdf", "report2.pdf"]
    initial_response = "Initial summary of the reports."
    user_question = "What about specific treatments?"
    model_answer = "The reports mention..."

    store_initial_response(session, files, initial_response)
    store_user_query(session, user_question)
    store_model_response(session, model_answer)

    history = get_conversation_history(session)
    for item in history:
        print(item)
