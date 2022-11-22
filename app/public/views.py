from flask import current_app, render_template, flash, redirect, request, url_for
from flask_login import login_user

from . import public
# from app.public.forms import LoginForm, RegisterUserForm
from app.extensions import lm
from app.data import User


@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@public.route('/')
def index():
    return render_template("public_index.html")

@public.route('/courses')
def courses():
    return render_template("public_courses.html")
