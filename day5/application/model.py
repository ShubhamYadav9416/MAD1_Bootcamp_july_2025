from .database import db
from flask_login import UserMixin
from sqlalchemy import event
from sqlalchemy.sql import func



class Users(db.Model,UserMixin):
    __tablename__ ="users"
    id = db.Column(db.Integer, primary_key = True)
    name  = db.Column(db.String(100))
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    is_active = db.Column(db.Boolean , default=True)
    address = db.Column(db.String(1000))
    is_librarian = db.Column(db.Boolean, default = False)
    
    def get_id(self):
        return str(self.id)
    
    
class Section(db.Model):
    __tablename__ = "section"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    description  =  db.Column(db.String(300))
    no_of_books = db.Column(db.Integer, default = 0)
    books = db.relationship("Book", back_populates = "sections",cascade='all, delete')
    

    
    
    
class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    author_name = db.Column(db.String(100), nullable = False)
    book_front_page_url = db.Column(db.String(100))
    section_id =  db.Column(db.Integer, db.ForeignKey("section.id"))
    
    sections = db.relationship("Section", back_populates = "books")
    
    
class RequestBooks(db.Model):
    __tablename__ = "requestedbook"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"),nullable = False)
    # status R = requested, D = declined, I = Issued, T = timeout or returned after been issued 
    status = db.Column(db.String(1), nullable = False)
    requested_time_period = db.Column(db.Integer, nullable = False)
    issued_time = db.Column(db.DateTime, default = func.now())
    
    
@event.listens_for(Book, 'after_insert')
def add_book(mapper, connection, target):
    section_id = target.section_id
    connection.execute(
        db.text("UPDATE section SET no_of_books = no_of_books + 1 WHERE id = :section_id"),
        {"section_id": section_id}
    )
    
@event.listens_for(Book, 'after_delete')
def add_book(mapper, connection, target):
    section_id = target.section_id
    connection.execute(
        db.text("UPDATE section SET no_of_books = no_of_books -1 WHERE id = :section_id"),
        {"section_id": section_id}
    )