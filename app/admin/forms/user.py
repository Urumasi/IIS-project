import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, EqualTo, Length

from app.fields import Predicate
from app.data import User


def username_is_available(username):
    if User.if_exists(username):
        return False
    return True

def safe_characters(s):
    if not s:
        return True
    return re.match(r'^[\w]+$', s) is not None


class UserForm(FlaskForm):
    username = StringField('Username', validators=[
        Predicate(safe_characters, message="Please use only letters and numbers"),
        Predicate(username_is_available, message="An account has already been registered with that name. Try another?"),
        Length(min=1, max=32, message="Please use between 1 and 32 characters"),
        InputRequired(message="This field is required")
    ])


class NewUserForm(UserForm):
    password = PasswordField('Password',validators=[
        InputRequired(message="This field is required"),
        Length(min=8, message="Please use at least 8 characters")
    ])

    confirm = PasswordField('Confirm Password', validators=[
        InputRequired(message="This field is required"),
        EqualTo('password', message='Passwords must match')
    ])


class EditUserForm(UserForm):
    username = StringField('Username')
    is_admin = BooleanField('Admin')
    active = BooleanField('Activated')