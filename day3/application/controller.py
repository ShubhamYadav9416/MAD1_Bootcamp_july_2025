from flask import current_app as app, render_template, url_for, redirect, flash, request

from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

from .model import db, Users, Section


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
        user =  Users.query.filter_by(email = email).first()
        if user is None:
            flash("email is not registered, Please register")
            print("user not found")
            return redirect("/register")
        else:
            if bcrypt.check_password_hash(user.password, password):
                print("correct password")
                login_user(user)
                if user.is_librarian == True:
                    print("lib dash")
                    return redirect("/librarian_dashboard")
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
# @login_required
def user_dashboard():
    return "this is user dashboard"


@app.route("/librarian_dashboard")
# @login_required
def librarian_dashboard():
    sections = Section.query.all()
    return render_template("librarian_dashboard.html", sections=sections)


@app.route("/add_new_section", methods = ["GET","POST"])
def add_new_section():
    if request.method == "GET":
        return render_template("add_section.html")
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        section = Section.query.filter_by(name = name).first()
        if section:
            flash("section name already exists")
            return redirect("/librarian_dashboard")
        new_section = Section(name = name , description = description)
        db.session.add(new_section)
        db.session.commit()
        flash("Section Added")
        return redirect("/librarian_dashboard")


@app.route("/logout")
# @login_required
def logout():
    login_user()
    return redirect("/")