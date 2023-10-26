from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)

#Pages in the website
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/shop.html")
def shop():
    return render_template("shop.html")

@app.route("/collections.html")
def collections():
    return render_template("collections.html")

@app.route("/categories.html")
def categories():
    return render_template("categories.html")

@app.route("/product.html")
def product():
    return render_template("product.html")

@app.route("/basket.html")
def basket():
    return render_template("basket.html")

# Redirect addresses
@app.route('/index.html')
def index():
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()