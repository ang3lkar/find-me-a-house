import requests
import config
import house_messages

class Client:

    ENDPOINT = 'https://graph.facebook.com/v2.6/me/messages/?access_token=' + config.FACEBOOK_TOKEN

    def __init__(self, type):
        self.type = type

    def send(self, user, house):
        image = house_messages.image_payload(user, house)
        requests.post(self.ENDPOINT, json=image)

        text = house_messages.text_payload(user, house)
        requests.post(self.ENDPOINT, json=text)
