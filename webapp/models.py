from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Users(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role_id = db.Column(db.Integer, db.ForeignKey('Roles.id'), default=1)
    role = db.relationship("Roles")
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())

class Roles(db.Model):
    __tablename__ = 'Roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(150))

class Cases(db.Model):
    __tablename__ = 'Cases'
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    role = db.Column(db.Integer, db.ForeignKey('Roles.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('Users.id'))
    system = db.Column(db.String(150))
    query_type = db.Column(db.String(150))
    description = db.Column(db.String(255))
    assigned_to = db.Column(db.Integer, db.ForeignKey('Users.id'))            
    current_progress = db.Column(db.Integer, db.ForeignKey('Current_Progress.id'))

class Query_Types(db.Model):
    __tablename__ = 'Query_Types'
    id = db.Column(db.Integer, primary_key=True)
    query_type = db.Column(db.String(150))
    
class Current_Progress(db.Model):
    __tablename__ = 'Current_Progress'
    id = db.Column(db.Integer, primary_key=True)
    current_progress = db.Column(db.String(150))


def build_roles():
    db.session.add(Roles(role="Admin"))
    db.session.add(Roles(role="Manager"))
    db.session.add(Roles(role="Caseworker"))
    db.session.add(Roles(role="User"))
    db.session.commit()


def build_categories():
    db.session.add(Query_Types(query_type="Functionality"))
    db.session.add(Query_Types(query_type="Hierarchy"))
    db.session.add(Query_Types(query_type="Deletions"))
    db.session.commit()
    
    
def build_current_progress():
    db.session.add(Current_Progress(current_progress='Outstanding'))
    db.session.add(Current_Progress(current_progress='Received'))
    db.session.add(Current_Progress(current_progress='User Contacted'))
    db.session.add(Current_Progress(current_progress='Resolved'))
    db.session.commit()
    
