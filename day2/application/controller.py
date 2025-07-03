from flask import current_app as app, render_template

@app.route('/')
def home():
    message = "passing message from controller"
    show_message = False
    return render_template("home.html", message=message, show_message=show_message)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")