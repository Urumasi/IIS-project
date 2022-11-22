from flask import current_app, render_template, redirect, url_for
from flask_login import login_required, logout_user, current_user

from . import auth
from app.extensions import lm
from app.data import User, Course

@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))

@auth.route('/my_courses')
@login_required
def my_courses():
    studied_c = Course.get_all_studied_courses(current_user.id)
    taught_c = Course.get_all_taught_courses(current_user.id)
    guaranteed_c = Course.get_all_guaranteed_courses(current_user.id)
    return render_template("courses.html",studied_c = studied_c , guaranteed_c = guaranteed_c, taught_c = taught_c)

@auth.route('/course_detail/<id>')
@login_required
def course_detail(id):
    course = Course.get_by_id(id)
    teachers = course.get_all_lecturers()
    return render_template("course_detail.html", course = course, teachers = teachers)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))
