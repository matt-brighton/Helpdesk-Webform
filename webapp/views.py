from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Users, Roles
from . import db
import json
from flask import jsonify

views = Blueprint('views', __name__)

# Home Screen
@ views.route('/')
def home():
    return render_template('home.html', user=current_user)

# Admin Screen
@ views.route('/admin', methods=['GET'])
def admin_table():
    page_id = request.args.get('page_id', 1, type = int)
    per_page = request.args.get('per_page', 10, type = int)
    data = Users.query.order_by(Users.created_date).paginate(page_id, per_page, False)
    return render_template('admin.html', user=current_user, data=data)

# New Request Screen
@ views.route('/new_request', methods=["GET"])
@login_required
def new_request():
    return render_template('new_request.html', user=current_user)


@ views.route('/admin', methods=['POST'])
def update():
    if request.method == 'POST':
        data = Users.query.get(request.form.get('idEdit'))
        data.first_name = request.form['NameEdit']
        data.email = request.form['EditEmail']
        db.session.commit()
        message = f"{data.first_name} Updated"
        flash(message)

    return redirect('/admin')


@ views.route('/delete_user', methods=['POST'])
def delete_user():
    if request.method == 'POST':  
        data = Users.query.get(request.form.get('idDelete'))
        db.session.delete(data)
        db.session.commit()
    return redirect('/')


