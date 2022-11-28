from flask import current_app, render_template, redirect, url_for
from flask_login import current_user

from . import admin
from app.util import admin_required
from app.extensions import lm
from app.data import User, CourseRequest

@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))

@admin.route('/admin')
@admin_required
def panel():
    count = CourseRequest.query.count()
    return render_template('panel.html', course_request_count=count)

@admin.route('/admin/new_user')
@admin_required
def new_user():
    return render_template('new_user.html')

@admin.route('/admin/course_requests')
@admin_required
def course_requests():
    requests = CourseRequest.query.all()
    return render_template('course_requests.html', requests=requests)
