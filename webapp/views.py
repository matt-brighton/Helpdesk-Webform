from datetime import datetime
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Users, Roles
from . import db
import json
from flask import jsonify

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')
