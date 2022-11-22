from flask import current_app, render_template, redirect, url_for
from flask_login import current_user

from . import admin
from app.util import admin_required
from app.extensions import lm
from app.data import User

@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))

@admin.route('/admin')
@admin_required
def panel():
    return render_template('panel.html')

@admin.route('/admin/new_user')
@admin_required
def new_user():
    return render_template('new_user.html')
