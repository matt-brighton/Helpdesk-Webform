from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Users, Roles
from . import db
import json
from flask import jsonify

views = Blueprint('views', __name__)


@ views.route('/')
def home():
    return render_template('home.html', user=current_user)



@ views.route('/admin', methods=['GET'])
def admin_table():  
    data = Users.query.order_by(Users.created_date)
    return render_template('admin.html', user=current_user, data=data)



@ views.route('/admin', methods=['POST'])
def update():
    if request.method == 'POST':
        data = Users.query.get(request.form.get('idEdit'))
        
        data.first_name = request.form['NameEdit']
        data.email = request.form['EditEmail']
        
        db.session.commit()
        flash("User details updated!")
        return redirect('/admin')
