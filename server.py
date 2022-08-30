import time
from flask import Flask, request, abort

app = Flask(__name__)
db = [
    {
        'text': 'hello',
        'name': 'Jack',
        'time': time.time()
    },
    {
        'text': 'hello, Jack',
        'name': 'John',
        'time': time.time()
    }
]
a = []
for i in db:
    a.append(i['name'])


@app.route("/")
def hello():
    return "Hello, Skillbox! <a href='/status'>Status</a>"


@app.route("/status")
def status():
    return {
        'status': True,
        'name': 'Skillbox Messenger',
        'time': time.time(),
        'number_of_users': str(len(set(a))),
        'number_of_messages': str(len(db))
    }


@app.route("/send", methods=['POST'])
def send_message():
    data = request.json

    # check data is dict with text & name
    if not isinstance(data, dict):
        return abort(400)
    if 'text' not in data or 'name' not in data:
        return abort(400)

    text = data['text']
    name = data['name']

    # check text & name are valid strings
    if not isinstance(text, str) or not isinstance(name, str):
        return abort(400)
    if len(text) == 0 or len(name) == 0:
        return abort(400)
    if len(text) > 1000 or len(name) > 100:
        return abort(400)

    message = {
        'text': text,
        'name': name,
        'time': time.time()
    }
    db.append(message)

    # if text == '/weather':
    #     db.append({
    #         'text': 'Ну сейчас дождя нет. Наверное',
    #         'name': 'Bot',
    #         'time': time.time()
    #     })

    return {'ok': True}


@app.route("/messages")
def get_messages():
    try:
        after = float(request.args['after'])
    except:
        return abort(400)

    result = []

    for message in db:
        if message['time'] > after:
            result.append(message)

    return {'messages': result[:100]}


app.run()
