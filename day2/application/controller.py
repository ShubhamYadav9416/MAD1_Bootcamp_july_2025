from flask import current_app as app, render_template, url_for, redirect, flash, request

from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

from .model import db, Users


bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)





@app.route('/')
def home():
    message = "passing message from controller"
    show_message = False
    return render_template("home.html", message=message, show_message=show_message)

@app.route("/login" , methods = ["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if email == "admin@gmail.com":
            if password == "1234":
                return redirect("/admin_dashboard")
        user =  Users.query.filter_by(email = email).first()
        if user is None:
            flash("email is not registered, Please register")
            return redirect("/register")
        else:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect("/user_dashboard")
            else:
                flash("Wrong Pasword")
                return redirect("/login")
            

@app.route("/register" , methods = ["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        
        user =  Users.query.filter_by(email = email).first()
        if user:
            flash("email already registered")
            return redirect("/login")
        else:
            password = request.form["password"]
            hashed_password = bcrypt.generate_password_hash(password)
            new_user = Users(name=  name, password = hashed_password, email= email)
            db.session.add(new_user)
            db.session.commit()
            flash("You are now registed please login")
            return redirect("/login")
        
        
        
@app.route("/user_dashboard")
def user_dashboard():
    return "this is user dashboard"


@app.route("/admin_dashboard")
def admin_dashboard():
    return "this is admin dashboard"