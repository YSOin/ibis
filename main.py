import requests
import json

from flask import jsonify
from flask import Flask
from flask import request
from parse import *

#https://api.telegram.org/bot1946897508:AAF-jzrzomGbn6GYB82aC653sFrrCTJ1F30/getUpdates
app = Flask(__name__)
token = '1946897508:AAF-jzrzomGbn6GYB82aC653sFrrCTJ1F30'

def generate_bot_method(token, method_variable):
    URL = f'https://api.telegram.org/bot{token}/{method_variable}'
    return URL

def write_json(data, filename='answer.json'):
    with open (filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def send_message(chat_id, text='Hello user'):
    url = generate_bot_method(token, 'sendMessage')
    answer = {'chat_id':chat_id, 'text':text}
    r = requests.post(url, json=answer)
    return r.json()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        try:
            doc = r['message']['document']
            send_message(chat_id, text='Я не принимаю файлы')
        except KeyError:
            message = r['message']['text']
            if 'ты' in message or 'Ты' in message:
                word = message.split(' ')
                send_message(chat_id, text=f'Сам ты {word[-1]}' )
            else:
                send_message(chat_id)

        write_json(r)
        return jsonify()
    return '<h1>Hello Main</h1>'
# def main():
#     pass    
    


if __name__ == '__main__':
    app.run()