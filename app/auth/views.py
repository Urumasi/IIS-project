from flask import current_app, render_template, redirect, url_for
from flask_login import login_required, logout_user, current_user

from . import auth
from app.extensions import lm
from app.data import User, Course, CourseRequest
from app.auth.forms import CreateCourseForm, ChangePasswordForm


@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@auth.route('/my_courses')
@login_required
def my_courses():
    studied_c = Course.get_all_studied_courses(current_user.id)
    taught_c = Course.get_all_taught_courses(current_user.id)
    guaranteed_c = Course.get_all_guaranteed_courses(current_user.id)
    all_c = Course.get_all()
    return render_template("courses.html", studied_c=studied_c, guaranteed_c=guaranteed_c, taught_c=taught_c, all_c = all_c)


@auth.route('/create_course', methods=['GET', 'POST'])
@login_required
def create_course():
    form = CreateCourseForm()
    if form.validate_on_submit():
        CourseRequest.create(
            requester=current_user.id,
            abbreviation=form.data["abbreviation"],
            description=form.data["description"],
            type=form.data["type"],
            price=form.data["price"],
            capacity=form.data["capacity"]
        )
        return redirect(url_for('auth.my_courses'))
    return render_template("course_create.html", form=form)


@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@auth.route('/change_password')
@login_required
def change_password():
    form = ChangePasswordForm(current_user)
    if form.validate_on_submit():
        current_user.set_password(form.data['new_password'])
        current_user.save()
        return redirect(url_for('auth.profile'))
    return render_template("change_password.html", form=form)


@auth.route('/course_detail/<id>')
@login_required
def course_detail(id):
    course = Course.get_by_id(id)
    teachers = course.get_all_lecturers()
    students = course.get_all_students()
    terms = course.get_all_terms()
    news = course.get_all_news()
    guaranthor = course.get_guarantor()
    user_type = ""

    if any(x for x in students if x.id == current_user.id):
        user_type = "student"
    elif any(x for x in teachers if x.id == current_user.id):
        user_type = "teacher"
    elif current_user.id == guaranthor.id:
        user_type = "guaranthor"   
    print(students)
    return render_template("course_detail.html", course = course, teachers = teachers, terms = terms, news = news, user_type = user_type, students = students)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))

@auth.route('/my_news')
@login_required
def my_news():
    news = current_user.get_all_news()
    # Maybe sort them by creation date or something lol
    return render_template('news_test.html', newz=news)
