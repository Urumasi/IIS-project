from flask import render_template

from . import public
from app.extensions import lm
from app.data import User

@lm.user_loader
def load_user(id):
        return User.get_by_id(int(id))

@public.route('/')
def index():
    return render_template("index.html")
