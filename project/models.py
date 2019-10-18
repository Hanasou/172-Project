from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from project import db, login_manager

bcrypt = Bcrypt()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    password = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    admin = db.Column(db.Boolean)

    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = bcrypt.generate_password_hash(password = password)
        if username == 'roy_zhang':
            self.admin = True
        else:
            self.admin = False

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class File(db.Model):

    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key = True)
    item = db.Column(db.String(64))
    user_fn = db.Column(db.String(64))
    user_ln = db.Column(db.String(64))
    upload_date = db.Column(db.TIMESTAMP)
    update_date = db.Column(db.TIMESTAMP)
    description = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, item, user_fn, user_ln, upload_date, update_date, description, user_id):
        self.item = item
        self.user_fn = user_fn
        self.user_ln = user_ln
        self.upload_date = upload_date
        self.update_date = update_date
        self.description = description
        self.user_id = user_id