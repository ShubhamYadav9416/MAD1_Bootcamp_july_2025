from .database import db
from flask_login import UserMixin


class Users(db.Model,UserMixin):
    __tablename__ ="users"
    id = db.Column(db.Integer, primary_key = True)
    name  = db.Column(db.String(100))
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    is_active = db.Column(db.Boolean)
    address = db.Column(db.String(1000))
    is_librarian = db.Column(db.Boolean, default = False)
    
    def get_id(self):
        return str(self.id)
    
    
class Section(db.Model):
    __tablename__ = "section"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    description  =  db.Column(db.String(300))
    
    books = db.relationship("Book", back_populates = "sections",cascade='all, delete')
    
    
    
class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    author_name = db.Column(db.String(100), nullable = False)
    book_front_page_url = db.Column(db.String(100))
    section_id =  db.Column(db.Integer, db.ForeignKey("section.id"))
    
    sections = db.relationship("Section", back_populates = "books")