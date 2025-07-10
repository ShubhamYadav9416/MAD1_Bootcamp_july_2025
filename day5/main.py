from flask import Flask

from application.database import db
from application.model import *

app = Flask(__name__, template_folder = "Template")

app.secret_key = "123456"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

app.app_context().push()

db.init_app(app)

from application.controller import *


def create_librarian():
    is_librarian_exist = Users.query.filter_by(is_librarian = True).first()
    if is_librarian_exist is None:
        add_librarian = Users(name = "Librarian", email = "librarian@gmail.com", password = bcrypt.generate_password_hash("1234"), is_librarian = True)
        db.session.add(add_librarian)
        db.session.commit()
        print("librarian got created")

with app.app_context():
    db.create_all()
    create_librarian()

if __name__ == "__main__":
    app.run(debug=True)