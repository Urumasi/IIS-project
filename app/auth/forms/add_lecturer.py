from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
from app.data import User


class AddLecturerForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired("This field is required")
    ])


    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)


    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        if not User.exists(self.username.data):
            self.username.errors.append('User does not exist')
            return False

        return True
