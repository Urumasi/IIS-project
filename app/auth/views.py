from flask import current_app, render_template, redirect, url_for
from flask_login import login_required, logout_user, current_user

from . import auth
from app.extensions import lm
from app.data import User

@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))

@auth.route('/test')
@login_required
def index():
    return render_template("test.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))
