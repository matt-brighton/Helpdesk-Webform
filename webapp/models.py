from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Users(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.Integer, db.ForeignKey('Roles.id'), default=1)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())


class Roles(db.Model):
    __tablename__ = 'Roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(150))


def build_roles():
    db.session.add(Roles(role="Admin"))
    db.session.add(Roles(role="Manager"))
    db.session.add(Roles(role="Caseworker"))
    db.session.add(Roles(role="User"))
    db.session.commit()
