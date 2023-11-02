from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('login_email')
        password = request.form.get('login_password')
        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login successful', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Invalid password', category='error')
        else:
            flash('Invalid email', category='error')

    return render_template("login.html", user=current_user)


@ auth.route('/logout')
@ login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@ auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up_form():

    if request.method == 'POST':

        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password = request.form.get('password')
        passwordconfirm = request.form.get('passwordconfirm')
        user = Users.query.filter_by(email=email).first()

        if user:
            flash('email already exists', category='error')
        elif len(email) < 4:
            flash('email must be at least 4 characters', category='error')
        elif len(firstname) < 2:
            flash('firstname must be at least 2 characters', category='error')
        elif password != passwordconfirm:
            flash('passwords do not match', category='error')
        elif len(password) < 7:
            flash('password must be at least 7 characters', category='error')

        else:
            new_user = Users(email=email, first_name=firstname,
                             password=generate_password_hash(password, method='sha256'))

            try:
                db.session.add(new_user)
                db.session.commit()

            except:
                flash("An error occurred, please contact IT if this problem continues", category='error')

            flash('Account Created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@ auth.route('/new_user', methods=['POST'])
def new_user():
    if request.method == 'POST':
        email = request.form.get('NewEmail')
        firstname = request.form.get('NewName')
        password = request.form.get('TempPassword')
        user = Users.query.filter_by(email=email).first()

        if user:
            flash('email already exists', category='error')
        elif len(email) < 4:
            flash('email must be at least 4 characters', category='error')
        elif len(firstname) < 2:
            flash('firstname must be at least 2 characters', category='error')
        elif len(password) < 7:
            flash('password must be at least 7 characters', category='error')

        else:
            new_user = Users(email=email, first_name=firstname,
                             password=generate_password_hash(password, method='sha256'))

            try:
                db.session.add(new_user)
                db.session.commit()

            except:
                flash("An error occurred, please contact IT if this problem continues", category='error')

            flash('Account Created!', category='success')
            return redirect(url_for('views.home'))

    return redirect(url_for('views.home'))
