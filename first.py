from flask import Flask, redirect, url_for, abort, request, render_template
import random
import string

app = Flask(__name__)

@app.route('/')
def hello_world():
    result = "<h1>The following is a random character:</h1>" + ''.join(random.choices(string.ascii_letters))
    return result

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

@app.route("/display/")
def display():
    return '<img src="'+url_for('static', filename='uploads/file.png')+'"/>'

@app.route("/upload/", methods=['POST','GET'])
def account():
    if request.method == 'POST':
        f = request.files['datafile']
        f.save('static/uploads/file.png')
        return "File Uploaded"
    else:
        page ='''
        <html><body>
        <form action="" method="post" name="form" enctype="multipart/form-data">
        <input type="file" name="datafile" />
        <input type="submit" name="submit" id="submit"/>
        </form>
        </body><html>'''
        return page, 200

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('conditional.html', name=name)

@app.route('/users/')
def users():
    names=['simon','thomas','lee','jamie','sylvester']
    return render_template('loops.html', names=names)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
