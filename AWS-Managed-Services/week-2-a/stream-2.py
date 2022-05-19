import logging
import json
from datetime import datetime
import calendar
import random
import time

logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(asctime)s %(message)s')



def put_to_stream(id, value, timestamp):
    payload = {
                'random': str(value),
                'timestamp': str(timestamp),
                'id': id
              }

    response ='Putting to stream: ' + str(payload)
    logging.debug(response)


while True:
    value = random.randint(1, 100)
    timestamp = calendar.timegm(datetime.utcnow().timetuple())
    id = 'v1'
    
    put_to_stream(id, value, timestamp)

    # wait for 5 second
    time.sleep(5)
