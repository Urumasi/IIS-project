from flask import current_app, render_template
from flask_login import login_user

from . import public
from app.extensions import lm
from app.data import User, Course


@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@public.route('/')
def index():
    return render_template("index.html")

@public.route('/courses')
def courses():
    return render_template("courses.html", courses = Course.get_all())
