import requests
import json
import traceback
import random
from os import environ
from flask import Flask, request

app = Flask(__name__)

token = environ['FACEBOOK_PAGE_ACCESS_TOKEN']

@app.route('/')
def index():
  return "Homepage"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
  if request.method == 'POST':
    try:
      data = json.loads(request.data)

      # Incoming Message Text
      text = data['entry'][0]['messaging'][0]['message']['text']

      # Sender ID
      sender = data['entry'][0]['messaging'][0]['sender']['id']

      # We're going to send this back
      payload = {'recipient': {'id': sender}, 'message': {'text': "Your sender_id is = {sender}".format(sender=sender)}}
      r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)

    except Exception as e:

  elif request.method == 'GET':
    # For the initial verification
    if request.args.get('hub.verify_token') == environ['FACEBOOK_VERIFY_TOKEN']:
      return request.args.get('hub.challenge')
    return "Wrong Verify Token"

  return "Hello World" # Not Really Necessary

if __name__ == '__main__':
  app.run(port=int(environ.get('PORT', 8080)), debug=True)
