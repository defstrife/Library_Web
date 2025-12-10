from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    role = db.Column(db.String(10), nullable = False) #admin, librarian, reader

class Author(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), nullable = False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable = False)
    genre = db.Column(db.String(20), nullable = False)
    available = db.Column(db.Boolean, default = True)
    author = db.relationship("Author", backref = "books")

class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable = False)
    order_date = db.Column(db.DateTime, default = datetime.utcnow)
    status = db.Column(db.String(20), default ='заказано')

class Issuance(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable = False)
    issuance_date = db.Column(db.DateTime, default = datetime.utcnow)
    return_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default = 'выдано')