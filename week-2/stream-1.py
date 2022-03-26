from http import client
import boto3
import json
from datetime import datetime
import calendar
import random
import time


kinesis_client = boto3.session.Session(region_name='us-east-1').client('kinesis', aws_access_key_id='XXXXXXXX', aws_secret_access_key='XXXXXXXXXXX')

my_stream_name = 'XXXX'

# kinesis_client = boto3.client('kinesis', region_name='us-east-1')

def put_to_stream(id, value, timestamp):
    payload = {
                'random': str(value),
                'timestamp': str(timestamp),
                'id': id
              }

    print('Putting to stream: ' + str(payload))

    put_response = kinesis_client.put_record(
                        StreamName=my_stream_name,
                        Data=json.dumps(payload),
                        PartitionKey=id)

while True:
    value = random.randint(1, 100)
    timestamp = calendar.timegm(datetime.utcnow().timetuple())
    id = 'stream-1'
    
    put_to_stream(id, value, timestamp)

    # wait for 5 second
    time.sleep(5)
