import requests
from os import environ

def send(house):

    try:
        token = environ['FACEBOOK_PAGE_ACCESS_TOKEN']
    except KeyError:
        print('Please set the environment variable FACEBOOK_PAGE_ACCESS_TOKEN')
        sys.exit(1)

    image_payload = {
      "recipient":{
        "id":"1198499103580071"
      },
      "message":{
        "attachment":{
          "type":"template",
          "payload":{
            "template_type":"generic",
            "elements":[
               {
                "title": house['location'],
                "image_url": house['image_url'],
                "subtitle": "{title} ({price})".format(title=house['title'], price=house['price']),
                "default_action": {
                  "type": "web_url",
                  "url": house['link'],
                  "messenger_extensions": False,
                  "webview_height_ratio": "tall"
                },
                "buttons":[
                  {
                    "type":"web_url",
                    "url": house['link'],
                    "title":"View Details"
                  }
                ]
              }
            ]
          }
        }
      }
    }
    r1 = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=image_payload)


    payload = {
        "message": {
            "text": house['body']
        },
        "recipient": {
            "id": "1198499103580071"
        }
    }
    r2 = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)
