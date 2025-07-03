from flask import Flask

from application.database import db
from application.model import *

app = Flask(__name__, template_folder = "Template")

app.secret_key = "123456"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

app.app_context().push()

db.init_app(app)

from application.controller import *

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)