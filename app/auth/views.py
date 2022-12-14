from flask import current_app, render_template, redirect, url_for, request
from flask_login import login_required, logout_user, current_user

from . import auth
from app.extensions import lm
import datetime

from app.data import User, Course, CourseRequest, StudyRequest, Term, TermBody, News, course_students
from app.auth.forms import CreateCourseForm, ChangePasswordForm, CreateTermForm, CreateNewsForm, AddLecturerForm, EditCourseForm


def get_user_type(course_id):
    course = Course.get_by_id(course_id)
    teachers = course.get_all_lecturers()
    students = course.get_all_students()
    guaranthor = course.get_guarantor()


    if current_user.id == guaranthor.id:
        return "guaranthor"
    elif any(x for x in teachers if x.id == current_user.id):
        return "teacher"
    elif any(x for x in students if x.id == current_user.id):
        return "student"
    else:
        return ""

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

@auth.route('/create_term/<id>', methods=['GET', 'POST'])
@login_required
def create_term(id):
    form = CreateTermForm()
    if form.validate_on_submit():
        Term.create(
            course = id,
            name = form.data["name"],
            type = form.data["type"],
            description = form.data["description"],
            date = form.data["date"],
            room = form.data["room"],
            max_body = form.data["max_body"]
        )
        return redirect(url_for('auth.course_detail', id=id))
    return render_template("term_create.html", form=form)

@auth.route('/create_news/<c_id>/<n_id>', methods=['GET', 'POST'])
@login_required
def create_news(c_id, n_id):
    news = News.get_by_id(n_id)
    if news:
        form = CreateNewsForm(da_newz=news.da_newz)
    else:
        form = CreateNewsForm()
        
    if form.validate_on_submit():
        if news:
            News.update(
                news,
                course = c_id,
                da_newz = form.data["da_newz"],
                created_ts = datetime.datetime.now()
            )
        else:
            News.create(
                course = c_id,
                da_newz = form.data["da_newz"],
                created_ts = datetime.datetime.now()
            )
        return redirect(url_for('auth.course_detail', id=c_id))
    return render_template("news_create.html", form=form, id=c_id)


@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(current_user)
    if form.validate_on_submit():
        current_user.set_password(form.data['new_password'])
        current_user.save()
        return redirect(url_for('auth.profile'))
    return render_template("change_password.html", form=form)


@auth.route('/course_detail/<id>', methods=['GET', 'POST'])
@login_required
def course_detail(id):
    course = Course.get_by_id(id)
    form = AddLecturerForm()
    if form.validate_on_submit():
        lecturer = User.find_by_name(form.data['username'])
        if not lecturer:
            return redirect(url_for('auth.course_detail', id=id))
        if not course.is_taught_by(lecturer):
            course.lecturers.append(lecturer)
            course.save()
        return redirect(url_for('auth.course_detail', id=id))
    teachers = course.get_all_lecturers()
    students = course.get_all_students()
    terms = course.get_all_terms()
    news = course.get_all_news()
    user_type = get_user_type(course.id)
    count_study_requests = StudyRequest.query.filter_by(course=id).count()

    return render_template("course_detail.html", form=form, course=course, teachers=teachers, terms=terms, news=news, user_type=user_type, students=students, count_study_requests=count_study_requests)

@auth.route('/edit_course/<id>', methods=['GET', 'POST'])
@login_required
def edit_course(id):
    course = Course.get_by_id(id)
    print(course.type)
    if course.type == 'in-person':
        select = 'in-person'
    else:
        select = 'distance'
    form = EditCourseForm(description=course.description, type=select, price=course.price, capacity=course.capacity)
    if form.validate_on_submit():
        Course.update(
            course,
            description = form.data["description"],
            type = form.data["type"],
            price = form.data["price"],
            capacity = form.data["capacity"],
        )
        return redirect(url_for('auth.course_detail', id=id))
    return render_template("course_edit.html", form=form)

@auth.route('/term_detail/<id>', methods=['GET', 'POST'])
@login_required
def term_detail(id):
    term = Term.get_by_id(id)
    course = Course.get_by_id(term.course)
    students = course.get_all_students()
    user_type = get_user_type(term.course)

    form = CreateTermForm(name=term.name, type=term.type, description=term.description, date=term.date, room=term.room, max_body=term.max_body)
    if form.validate_on_submit():
        Term.update(
            term,
            course=term.course,
            name=form.data["name"],
            type=form.data["type"],
            description=form.data["description"],
            date=form.data["date"],
            room=form.data["room"],
            max_body=form.data["max_body"]
        )
        return redirect(url_for('auth.course_detail', id=term.course))
    return render_template("term_detail.html", term=term, user_type=user_type, students=students, form=form)


@auth.route('/delete_term/<id>')
@login_required
def delete_term(id):
    delete = Term.get_by_id(id)
    ret = Term.get_by_id(id)
    if delete:
        delete.del_term()
    return redirect(url_for('auth.course_detail', id=ret.course))


@auth.route('/delete_news/<id>')
@login_required
def delete_news(id):
    delete = News.get_by_id(id)
    ret = News.get_by_id(id)
    if delete:
        delete.del_news()
    return redirect(url_for('auth.course_detail', id=ret.course))


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


@auth.route('/register_course/<id>')
@login_required
def register_course(id):
    course = Course.get_by_id(id)
    if course.is_studied_by(current_user):
        return redirect(url_for('auth.my_courses'))
    request = StudyRequest.find_existing(current_user, course)
    if request:
        return redirect(url_for('auth.my_courses'))
    StudyRequest.create(
        requester=current_user.id,
        course=course.id
    )
    return redirect(url_for('auth.my_courses'))

@auth.route('/study_requests/<id>')
@login_required
def study_requests(id):
    course = Course.get_by_id(id)
    requests = StudyRequest.query.filter_by(course=id).all()
    count_registered = Course.query.join(course_students).filter_by(course_id=id).count()
    return render_template('study_requests.html', course=course, requests=requests, count_registered=count_registered)

@auth.route('/accept_study/<id>')
@login_required
def accept_study(id):
    request = StudyRequest.get_by_id(id)
    if request:
        cid = request.course
        request.accept()
        return redirect(url_for('auth.study_requests', id=cid))
    return redirect(url_for('auth.my_courses'))

@auth.route('/reject_study/<id>')
@login_required
def reject_study(id):
    request = StudyRequest.get_by_id(id)
    if request:
        cid = request.course
        request.reject()
        return redirect(url_for('auth.study_requests', id=cid))
    return redirect(url_for('auth.my_courses'))


@auth.route('/api/change_points', methods=['POST'])
@login_required
def api_change_points():
    if not request.is_json:
        return '{"status": "error", "content": "Unknown method"}'
    try:
        user_id = int(request.json['user'])
    except ValueError:
        return '{"status": "error", "content": "Invalid user id"}'
    try:
        term_id = int(request.json['term'])
    except ValueError:
        return '{"status": "error", "content": "Invalid term id"}'
    try:
        points = int(request.json['points'])
    except ValueError:
        return '{"status": "error", "content": "Invalid points format"}'
    
    term: Term = Term.get_by_id(term_id)
    if not term:
        return '{"status": "error", "content": "Term not found"}'
    user: User = User.get_by_id(user_id)
    if not user:
        return '{"status": "error", "content": "User not found"}'

    if points < 0 or points > term.max_body:
        return '{"status": "error", "content": "Points out of bounds"}'

    course: Course = Course.get_by_id(term.course)
    if not course:
        return '{"status": "error", "content": "Course not found"}'
    
    if not course.is_taught_by(current_user):
        return '{"status": "error", "content": "Unauthorized access to course"}'
    
    points_object : TermBody = TermBody.get_by_ids(user.id, term.id)
    if points_object:
        points_object.body = points
    else:
        points_object = TermBody(
            user_id=user.id,
            term_id=term.id,
            body=points
        )
    points_object.save()
    return '{"status": "success", "content": "Points updated"}'
