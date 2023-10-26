from flask import Flask, flash, redirect, request, url_for, render_template

app = Flask(__name__)
app.secret_key = 'supersecret'
# Key above is just and example, it can be genrated by doing the following:
# >>> import os
# >>> os.urandom(24)
# Then paste result in string above

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/')
@app.route('/login/<message>')
def login(message=None):
    if (message != None):
        flash(message)
    else:
        flash(u'A default message')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
