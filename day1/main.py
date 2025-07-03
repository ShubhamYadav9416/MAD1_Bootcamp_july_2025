from flask import Flask

app = Flask(__name__, template_folder = "Template")

app.secret_key = "123456"
app.app_context().push()

from application.controller import *

if __name__ == "__main__":
    app.run(debug=True)