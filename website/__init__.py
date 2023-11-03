from flask import Flask, flash, redirect, url_for, render_template, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

# Dummy user data (to replace with a database in a real application) -- not being used so far --
#registered_users = {"giacob500@gmail.com": "Giacomo", "jianingzhang.zjn@gmail.com": "Jiajiolina Piccolina Magica Amorino Xiaolina", "test@test.net": "test"}

# Testing
@app.route("/test")
def test():
    return render_template("examples/selectionmenu.html")

#Pages in the website
@app.route("/homepage")
@app.route("/home")
@app.route("/index")
@app.route("/")
def home():
    if "user" in session:
        return render_template("index.html", username=session["user"])
    return render_template("index.html")

@app.route("/categories")
def categories():
    if "user" in session:
        return render_template("categories.html")
    flash("Please log-in to access this page", "info")
    return redirect(url_for("login"))

@app.route("/collections")
def collections():
    if "user" in session:
        return render_template("collections.html")
    flash("Please log-in to access this page", "info")
    return redirect(url_for("login"))

@app.route("/product")
def product():
    if "user" in session:
        return render_template("product.html")
    flash("Please log-in to access this page", "info")
    return redirect(url_for("login"))

@app.route("/basket")
def basket():
    if "user" in session:
        return render_template("basket.html")
    flash("Please log-in to access this page", "info")
    return redirect(url_for("login"))

# Check if user is loggin in for the first time or is already logged in
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True 
        user = request.form["email"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("You are already logged in as " + user, "info")
            return redirect(url_for("user"))
        return render_template("login.html")
    
# Check if user is already logged in, otherwise prompt login screen
@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return redirect(url_for("home"))
        #return render_template("categories.html", username=registered_users.get(usr, "User"))
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
    session.pop("user", None)
    return redirect(url_for("home"))

# Error handler 404
@app.errorhandler(404)
def invalid_route(e):
    return render_template("error404.html")

if __name__ == "__main__":
    app.run(debug=True)