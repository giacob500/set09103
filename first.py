from flask import Flask, redirect, url_for, abort
import random
import string
app = Flask(__name__)

@app.route('/')
def hello_world():
    result = "<h1>The following is a random character:</h1>" + ''.join(random.choices(string.ascii_letters))
    return result

@app.route("/hello/")
def hello():
    return "Hello Napier!!! :D"

@app.route("/private")
def private():
    #Test for user logged in failed so redirect to login URL
    return redirect (url_for('login'))

@app.route('/login')
def login():
    return "Now we would get username & password"

@app.route('/force404')
def force404():
    abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return "Couldn't find the page you requested.", 404

@app.route('/static-example/img')
def static_example_img():
    start = '<img src="'
    url = url_for('static', filename='vmask.jpg')
    end = '">'
    return start+url+end, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
