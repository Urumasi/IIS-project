from flask import current_app, render_template, redirect, request, url_for
from flask_login import login_user

from . import public
from app.extensions import lm
from app.data import User, Course
from app.public.forms import LoginForm


@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@public.route('/')
def index():
    print(Course.get_all())
    return render_template("index.html")

@public.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        return redirect(request.args.get('next') or url_for('public.index'))
    return render_template('login.html', form=form)
