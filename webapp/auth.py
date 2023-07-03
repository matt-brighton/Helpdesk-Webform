from flask import Blueprint, render_template, request, flash, redirect, url_for
# from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint('auth', __name__)


