from flask import Flask, flash, redirect, url_for, render_template, request, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "notasecret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../var/users.sqlite3'
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=15)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    category = db.Column(db.String(255))
    image_url = db.Column(db.String(255))

# Testing
@app.route("/test")
def test():
    return render_template("examples/test1.html")

@app.route("/admin")
def adminview():
    if "email" in session and session["email"] == "lorenzi@lorenzi.net":
        return render_template("admin_view.html", values=users.query.all())
    flash("Please log-in to access this page", "info")
    return redirect(url_for("login"))

#Pages in the website
@app.route("/homepage")
@app.route("/home")
@app.route("/index")
@app.route("/")
def home():
    if "email" in session:
        return render_template("index.html", username=session["email"])
    return render_template("index.html")

@app.route("/categories", methods=["POST", "GET"])
def categories():
    if "email" in session:
        if request.method == "POST":
            product_type = request.form["product_type"]
            product_counter = int(request.form["product_counter"])
            selected_tiles = request.form["selected_tiles"]
            product_quantity = int(request.form["product_quantity"])

            # Store the data in the session
            product_data = {
                "product_type": product_type,
                "product_counter": product_counter,
                "selected_tiles": selected_tiles,
                "product_quantity": product_quantity
            }
            
            # Check if the "product_data" list is already in the session, if not, initialize it
            if "basket_data" not in session:
                session["basket_data"] = []
            session["basket_data"].append(product_data)
            return redirect(url_for("categories"))

        return render_template("categories.html")
    flash("Please log-in to access this page", "info")
    return redirect(url_for("login"))

@app.route("/collections", methods=["POST", "GET"])
def collections():
    if "email" in session:
        if request.method == "POST":
            chosen_category = request.form["category"]
            products = Products.query.filter_by(category=chosen_category.lower()).all()
            return render_template("collections.html", chosen_category=chosen_category, products=products)
    flash("Please log-in to access this page", "info")
    return redirect(url_for("login"))

@app.route("/product", methods=["POST", "GET"])
def product():
    if "email" in session:
        if request.method == "POST":
            chosen_product = request.form["collection"]
            return render_template("product.html", chosen_product=chosen_product)
        # return render_template("product.html")
    flash("Please log-in to access this page", "info")
    return redirect(url_for("login"))

@app.route("/basket", methods=["POST", "GET"])
def basket():
    if "email" in session:
        if request.method == "POST" and 'reset' in request.form:
            session.pop("basket_data", None)
            return redirect(url_for("basket"))
        if "basket_data" in session:
            return render_template("basket.html", basket_data=session["basket_data"])
        return render_template("basket.html")
    flash("Please log-in to access this page", "info")
    return redirect(url_for("login"))

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['pswd']
        new_user = users(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

# Check if user is loggin in for the first time or is already logged in
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True 
        email = request.form["email"]
        password = request.form["pswd"]
        found_user = users.query.filter_by(email=email).first()
        # Check if there is any corresponding user in db
        if found_user:
            if found_user.email == email and found_user.password == password:
                session["email"] = found_user.email
                # Login successful
                return redirect(url_for('user'))
        else:
            flash('Login Failed, please check email and password.', 'error')
        return render_template("login.html")
    else:
        # If there is already an email in the session and it corresponds to an email in the db
        if "email" in session and users.query.filter_by(email=session["email"]).first():
            flash("You are already logged in", "info")
            return redirect(url_for("user"))
        return render_template("login.html")
    
# Check if user is already logged in, otherwise prompt login screen
@app.route("/user")
def user():
    # If there is already an email in the session and it corresponds to an email in the db
    if "email" in session and users.query.filter_by(email=session["email"]).first():
        return redirect(url_for("home"))
        #return render_template("categories.html", username=registered_users.get(usr, "User"))
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("email", None)
    # Clear the flashed messages in the list by flashing an empty message
    session.pop('_flashes', None)
    session.pop("basket_data", None)
    return redirect(url_for("home"))

# Error 404 handler
@app.errorhandler(404)
def invalid_route(e):
    return render_template("error404.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)