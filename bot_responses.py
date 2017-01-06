from os import environ
import requests
import models
import config


class BotResponses:

    def __init__(self, data):
        self.sender_id = data['entry'][0]['messaging'][0]['sender']['id']
        self.message = data['entry'][0]['messaging'][0]['message']['text']
        self.name = self._get_name()

    def setup_user(self):
        user, created = models.User.get_or_create(
            sender_id=self.sender_id, name=self.name)
        if not user.url:
            self._ask_url()
        else:
            self._greet_user()

    def set_url(self):
        user, created = models.User.get_or_create(sender_id=self.sender_id)
        user.url = self.message
        user.save()

        payload = {
            'recipient': {'id': self.sender_id},
            'message': {'text': 'Got it, I will be bothering you with new ads. Good luck ;)'.
                                format(name=self.name)}
        }
        self.send(payload)

    def warning(self):
        payload = {
            'recipient': {'id': self.sender_id},
            'message': {'text': 'Send me a valid search URL'.format(name=self.name)}
        }
        self.send(payload)

    # private

    def _greet_user(self):
        payload = {'recipient': {'id': self.sender_id}, 'message': {
            'text': "Hello {name}! Your sender_id is = {sender_id}".format(
                name=self.name, sender_id=self.sender_id)}}
        self.send(payload)

    def _get_name(self):
        response = requests.get(
            'https://graph.facebook.com/{id}?access_token={token}'.format(
                id=self.sender_id, token=config.FACEBOOK_TOKEN)).json()
        return response['first_name'] + ' ' + response['last_name']

    def _ask_url(self):
        payload = {
            'recipient': {'id': self.sender_id},
            'message': {'text': 'Hello {name}, please provide me with the bookmarked xe.gr URL'.
                                format(name=self.name)}
        }
        self.send(payload)

    def send(self, payload):
        requests.post(
            'https://graph.facebook.com/v2.6/me/messages/?access_token=' + config.FACEBOOK_TOKEN, json=payload)

