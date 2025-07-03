from .database import db

class Users(db.Model):
    __tablename__ ="users"
    id = db.Column(db.Integer, primary_key = True)
    name  = db.Column(db.String(100))
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)