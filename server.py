from os import environ
import json
import requests
import models

from flask import Flask, request

app = Flask(__name__)

TOKEN = environ['FACEBOOK_PAGE_ACCESS_TOKEN']


@app.route('/')
def index():
    return "Homepage"


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)

            # Sender ID
            sender_id = data['entry'][0]['messaging'][0]['sender']['id']

            response = requests.get(
                'https://graph.facebook.com/{id}?fields=name&access_token={token}'.format(
                    id=sender_id, token=TOKEN))
            name = json.loads(response)['name']

            print('Creating new user {name} with sender_id {sender_id}'.format(
                name=name, sender_id=sender_id))
            user = models.User(name=name, sender_id=sender_id)
            user.save()

            # We're going to send this back
            payload = {'recipient': {'id': sender_id}, 'message': {
                'text': "Hello {name}! Your sender_id is = {sender_id}".format(
                    name=name, sender_id=sender_id)}}

            requests.post(
                'https://graph.facebook.com/v2.6/me/messages/?access_token=' + TOKEN, json=payload)

        except Exception as e:
            print(e)

    elif request.method == 'GET':
        # For the initial verification
        if request.args.get('hub.verify_token') == TOKEN:
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"

    return "Hello World"  # Not Really Necessary


if __name__ == '__main__':
    app.run(port=int(environ.get('PORT', 8080)), debug=True)
