from flask import current_app, render_template

from . import auth
from app.extensions import lm
from app.data import User

@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@auth.route('/test')
def index():
    return render_template("test.html")
