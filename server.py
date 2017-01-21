from os import environ
from Flask import Flask

app = Flask(__name__)
app.run(environ.get('PORT'))

