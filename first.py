from flask import Flask
import random
import string
app = Flask(__name__)

@app.route('/')
def hello_world():
    result = "<h1>The following is a random character:</h1>" + ''.join(random.choices(string.ascii_letters))
    return result
