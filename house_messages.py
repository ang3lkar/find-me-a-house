def image_payload(user, house):
    return {
        "recipient": {
            "id": user.sender_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": house.location,
                            "image_url": house.image_url,
                            "subtitle": "{title} ({price})".format(title=house.title, price=house.price),
                            "default_action": {
                                "type": "web_url",
                                "url": house.link,
                                "messenger_extensions": False,
                                "webview_height_ratio": "tall"
                            },
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": house.link,
                                    "title": "View Details"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }

def text_payload(user, house):
    return {
        "message": {"text": house.body},
        "recipient": {"id": user.sender_id}
    }
