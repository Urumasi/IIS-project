import re
from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import InputRequired, EqualTo, Length


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Current password', validators=[
        InputRequired("This field is required")
    ])

    new_password = PasswordField('New password',validators=[
        InputRequired(message="This field is required"),
        Length(min=8, message="Please use at least 8 characters")
    ])

    confirm = PasswordField('Confirm password', validators=[
        InputRequired(message="This field is required"),
        EqualTo('password', message='Passwords must match')
    ])


    def __init__(self, user, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = user


    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append('Incorrect password')
            return False

        return True
