from flask import Flask, redirect, url_for, render_template, request
app = Flask(__name__)

# Testing
@app.route("/test")
def test():
    return render_template("examples/test.html")

#Pages in the website
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/shop")
def shop():
    return render_template("shop.html")

@app.route("/collections")
def collections():
    return render_template("collections.html")

@app.route("/categories")
def categories():
    return render_template("categories.html")

@app.route("/product")
def product():
    return render_template("product.html")

@app.route("/basket")
def basket():
    return render_template("basket.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["email"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return redirect(url_for('home'))

# Redirect addresses
@app.route('/index.html')
def index():
    return redirect(url_for('home'))

# Error handler 404
@app.errorhandler(404)
def invalid_route(e):
    return render_template("error404.html")

if __name__ == "__main__":
    app.run(debug=True)