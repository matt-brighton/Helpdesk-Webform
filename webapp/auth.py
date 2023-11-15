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


# Defines the route for signup with http methods of POST and GET, calls the function sign_up_form()
@ auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up_form():
    
    # if the request method is POST, then take information from the form (email, firstname, password, passwordconfirm)
    # and declare a variable of 'user' by checking querying the database to check if the email already exists.
    if request.method == 'POST':

        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password = request.form.get('password')
        passwordconfirm = request.form.get('passwordconfirm')
        user = Users.query.filter_by(email=email).first()

        # if the user already exists, throw a message on screen 
        if user:
            flash('email already exists', category='error')
        
        # if the email is less than 4 characters, throw a message on screen
        elif len(email) < 4:
            flash('email must be at least 4 characters', category='error')
        
        # if the first name is less than 2 characters, throw a message on screen
        elif len(firstname) < 2:
            flash('firstname must be at least 2 characters', category='error')
        
        # PASSWORD SECURITY
        # if password and password confirm don't match, throw an error on screen
        elif password != passwordconfirm:
            flash('passwords do not match', category='error')
        # if the length of the password is less that 7 characters, throw and error
        elif len(password) < 7:
            flash('password must be at least 7 characters', category='error')
        # if there aren't any upper case characters, throw an error
        elif not any(char.isupper() for char in password):
            flash('Password must contain at least one uppercase letter', category='error')
        # if there aren't any lower case characters, throw an error
        elif not any(char.islower() for char in password):
            flash('Password must contain at least one lowercase letter', category='error')
        # if there are no digits in the password, throw an error
        elif not any(char.isdigit() for char in password):
            flash('Password must contain at least one digit', category='error')
        # if there are no special characters, throw an error
        elif not any(char in '!@#$%^&*()-_=+[]{}|;:\'",.<>?/`~' for char in password):
            flash('Password must contain at least one special character', category='error')

        # if all conditions are met, assign a variable new_user the email, first name and password.
        # for an extra layer of security, the generate_password_hash function is used, which encrypts
        # the password in the database. 
        else:
            new_user = Users(email=email, first_name=firstname,
                             password=generate_password_hash(password, method='sha256'))

            # add and commit the new user to the database
            try:
                db.session.add(new_user)
                db.session.commit()

                # if successful, then confirm to the user that the account has been created, log the user in and redirect to the home page
                flash('Account Created!', category='success')
                login_user(new_user, remember=True)
                return redirect(url_for('views.home'))
            
            # if unsuccessful, throw an exception. This exception will provide the user with
            # a specified message, depending on the situation.
            except Exception as exception:
                db.session.rollback()
                flash(f'An error occurred: {str(exception)}', category='error')
        
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
