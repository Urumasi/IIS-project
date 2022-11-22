from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from app.data import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("This field is required")])
    password = PasswordField('Password', validators=[DataRequired("This field is required")])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None


    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        self.user = User.find_by_name(self.username.data)
        if not self.user:
            self.username.errors.append('User not found')
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append('Incorrect password')
            return False

        if not self.user.active:
            self.username.errors.append('This user has been disabled by an administrator')
            return False

        return True
