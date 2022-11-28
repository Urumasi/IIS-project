from flask_wtf import FlaskForm
import datetime
from wtforms import StringField, RadioField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, NumberRange


class CreateNewsForm(FlaskForm):
    da_newz = StringField('Text', validators=[DataRequired("This field is required")])


    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
    
        return True
