from . import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Notes(db.Model):
    __tablename__ = 'Notes'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(10000))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

class Cases(db.Model):
    __tablename__ = 'Cases'
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    role_id = db.Column(db.Integer, db.ForeignKey('Roles.id'))
    role = db.relationship("Roles")
    created_by_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    created_by = db.relationship("Users", foreign_keys=[created_by_id])
    system_id = db.Column(db.Integer, db.ForeignKey('Systems.id'))
    system = db.relationship("Systems")
    query_type_id = db.Column(db.Integer, db.ForeignKey('Query_Types.id'))
    query_type = db.relationship("Query_Types")
    description = db.Column(db.String(255))
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    assigned_to = db.relationship("Users", foreign_keys=[assigned_to_id])           
    current_progress_id = db.Column(db.Integer, db.ForeignKey('Current_Progress.id'), default=1)
    current_progress = db.relationship("Current_Progress")

class Users(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role_id = db.Column(db.Integer, db.ForeignKey('Roles.id'), default=1)
    role = db.relationship("Roles")
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_cases = db.relationship("Cases", foreign_keys=[Cases.created_by_id])
    assigned_cases = db.relationship("Cases", foreign_keys=[Cases.assigned_to_id])
    user_notes = db.relationship('Notes')

class Query_Types(db.Model):
    __tablename__ = 'Query_Types'
    id = db.Column(db.Integer, primary_key=True)
    query_type = db.Column(db.String(150))
    
class Current_Progress(db.Model):
    __tablename__ = 'Current_Progress'
    id = db.Column(db.Integer, primary_key=True)
    current_progress = db.Column(db.String(150))
    
class Systems(db.Model):
    __tablename__ = 'Systems'
    id = db.Column(db.Integer, primary_key=True)
    system = db.Column(db.String(150))
    
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
    
def build_systems():
    db.session.add(Systems(system='CRMM'))
    db.session.add(Systems(system='Caseflow'))
    db.session.add(Systems(system='CRMM'))
    db.session.add(Systems(system='ETMP'))
    db.session.add(Systems(system='RHS'))
    db.session.commit()
    
