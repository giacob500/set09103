from flask import Flask, flash, redirect, url_for, render_template, abort, request, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


#---- APP CONFIGURATION ----

app = Flask(__name__)
app.config["SECRET_KEY"] = "not_a_secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../var/db.sqlite3"
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=15)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#---- DATABASE CONFIGURATION ----

class Users(db.Model):
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

#---- ERROR HANDLING ----

# Define a custom error handler for all server errors (5xx)
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("error.html", error_message="Internal Server Error"), 500

# Define a custom error handler for client error 404
@app.errorhandler(404)
def invalid_route(e):
    return render_template("error.html", error_message="The source you are looking forward does not exist. Please return to the homepage."), 404

# Define a custom error handler for all other errors
@app.errorhandler(Exception)
def handle_all_errors(e):
    return render_template("error.html", error_message="An unexpected error occurred"), 500

#---- TESTING ----

# Route to simulate an error (for testing purposes)
@app.route("/simulate_error")
def simulate_error():
    raise Exception(404)

# Route to simulate a 404 error (for testing purposes)
@app.route('/simulate_error_404')
def simulate_error_404():
    abort(404)

# Testing
@app.route("/test")
def test():
    return render_template("examples/paragraph.html")

#---- ROUTING AND PAGES ----

@app.route("/admin")
def adminview():
    if "email" in session and session["email"] == "lorenzi@lorenzi.net":
        return render_template("admin_view.html", values=Users.query.all())
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
            # If no tile selection has been made, include the whole set in the basket
            product_name = request.form["product_name"]
            product_type = request.form["product_type"]
            if request.form["product_counter"] == "":
                product_counter = 4
                selected_tiles = "Tile 1, Tile 2, Tile 3, Tile 4"
            else:
                product_counter = int(request.form["product_counter"])
                selected_tiles = request.form["selected_tiles"]
            product_quantity = int(request.form["product_quantity"])
            
            # Store the data in the session
            product_data = {
                "product_name": product_name,
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
            print
            chosen_product_url = request.form["product_image_url"]
            chosen_product_name = request.form["product_name"]
            print(str(chosen_product_url + " " + chosen_product_name))
            return render_template("product.html", chosen_product_url=chosen_product_url, chosen_product_name=chosen_product_name)
    flash("Please log-in to access this page", "info")
    return redirect(url_for("login"))

@app.route("/basket", methods=["POST", "GET"])
def basket():
    if "email" in session:
        if request.method == "POST":
            #Empty basket
            if "reset" in request.form:
                session.pop("basket_data", None)
            #Delete single element from basket
            elif "remove" in request.form:
                to_remove = request.form["remove"]
                substrings = to_remove.split("-")
                matching_item = None
                for item in session.get("basket_data", []):
                    print(str(item))
                    if (
                        str(item.get("product_name")) == substrings[0]
                        and str(item.get("product_type")) == substrings[1]
                        and str(item.get("product_counter")) == substrings[2]
                        and str(item.get("selected_tiles")) == substrings[3]
                        and str(item.get("product_quantity")) == substrings[4]
                    ):
                        matching_item = item
                        break
                if matching_item:
                    session["basket_data"].remove(matching_item)
            return redirect(url_for("basket"))
        if "basket_data" in session:
            return render_template("basket.html", basket_data=session["basket_data"])
        return render_template("basket.html")
    flash("Please log-in to access this page", "info")
    return redirect(url_for("user"))

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if "email" in session:
            return redirect(url_for("user"))
        print("does it go in?")
        
        email = request.form["email"]
        password = request.form["pswd"]

        # Check if the email is already in use
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already in use. Please choose another email.", "error")
            return redirect(url_for("register"))

        if not password:  # Check if the password is empty
            flash("Password cannot be empty. Please insert a password.", "error")
            return redirect(url_for("register"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = Users(email=email, password=hashed_password)
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

        # Check if there is any corresponding email in db
        found_user = Users.query.filter_by(email=email).first()
        if found_user and bcrypt.check_password_hash(found_user.password, password):
            # Login successful
            session["email"] = found_user.email
            return redirect(url_for("user"))
        else:
            flash("Login Failed, please check email and password.", "error")
        return render_template("login.html")
    # If there is already an email in the session check who they are
    if "email" in session:
        return redirect(url_for("user"))
    return render_template("login.html")
    
# Check if user is already logged in, otherwise prompt login screen
@app.route("/user")
def user():
    # If there is already an email in the session and it corresponds to an email in the db
    if "email" in session and Users.query.filter_by(email=session["email"]).first():
        return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("email", None)
    # Clear the flashed messages in the list by flashing an empty message
    session.pop("_flashes", None)
    session.pop("basket_data", None)
    return redirect(url_for("home"))



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)