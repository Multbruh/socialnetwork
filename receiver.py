import time
from datetime import datetime
import requests


def print_messages(messages):
    for message in messages:
        print(
            datetime.fromtimestamp(message['time']),
            message['name']
        )
        print(message['number_of_users'], message['number_of_messages'])
        print(message['text'])
        print()


after = 0

while True:
    r = requests.get(
        'http://127.0.0.1:5000/messages',
        params={'after': after}
    )

    messages = r.json()['messages']
    if messages:
        print_messages(messages)
        after = messages[-1]['time']

    time.sleep(1)
