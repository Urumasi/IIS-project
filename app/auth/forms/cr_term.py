from flask_wtf import FlaskForm
import datetime
from wtforms import StringField, RadioField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, NumberRange


class CreateTermForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired("This field is required")])
    type = StringField('Type', validators=[DataRequired("This field is required")])
    description = StringField('Description', validators=[DataRequired("This field is required")])
    date = DateField('Deadline', validators=[DataRequired("This field is required")], format='%Y-%m-%d')
    room = StringField('Room', validators=[DataRequired("This field is required")])
    max_body = IntegerField('Maximum of points', validators=[DataRequired("This field is required"), NumberRange(min=0, max=100)])


    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        
        now = datetime.date.today()
        if now < self.date.data:
            return True
