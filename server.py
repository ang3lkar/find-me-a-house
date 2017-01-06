from os import environ
import json
import config
from bot_responses import BotResponses

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return "Homepage"


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            res = BotResponses(data)

            if 'xe.gr' in res.message:
                if 'xe.gr/property/search' in res.message:
                    res.set_url()
                else:
                    res.warning()
            else:
                res.setup_user()

        except Exception as e:
            print(e)

    elif request.method == 'GET':
        # For the initial verification
        if request.args.get('hub.verify_token') == config.FACEBOOK_TOKEN:
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"

    return "Hello World"  # Not Really Necessary


if __name__ == '__main__':
    app.run(port=int(environ.get('PORT', 8080)), debug=True)
