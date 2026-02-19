from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(42), unique = True, nullable = False)
    passhash = db.Column(db.String(512), nullable = False)
    name = db.Column(db.String(120), nullable= False)
    is_admin = db.Column(db.Boolean, nullable = False, default = False)
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self,password):
        self.passhash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.passhash,password)

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(63), nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Float, nullable = False)
    man_date = db.Column(db.Date, nullable = False)
    carts = db.relationship("Cart", backref='product', lazy = True)
    orders = db.relationship("Order", backref="product", lazy= True)

class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(66), nullable = False)

    products = db.relationship("Product", backref = "category", lazy = True)

class Cart(db.Model):
    __tablename__= "cart"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key = True)
    transaction_id = db.Column(db.Integer, db.ForeignKey("transaction.id"), nullable =False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Float, nullable =False)


class Transaction(db.Model):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key = True)
    datetime = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    total = db.Column(db.Float, nullable = False)
    orders = db.relationship("Order", backref = "transaction", lazy = True)
    

