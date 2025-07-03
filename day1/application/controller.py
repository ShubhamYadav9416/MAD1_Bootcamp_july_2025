from flask import current_app as app, render_template

@app.route('/home')
def home():
    message = "passing message from controller"
    show_message = False
    return render_template("home.html", message=message, show_message=show_message)