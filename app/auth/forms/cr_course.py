from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, IntegerField
from wtforms.validators import DataRequired, Length
from app.data import Course


class CreateCourseForm(FlaskForm):
    abbreviation = StringField('Abbreviation', validators=[DataRequired("This field is required"), Length(min=3, max=5,
                                                                                                          message="Abbreviation should be between 3 and 5 characters long!")])
    description = StringField('Description', validators=[DataRequired("This field is required")])
    type = RadioField('Select type', validators=[DataRequired("This field is required")],
                      choices=[('in-person', 'In-person'), ('distance', 'Distance')], validate_choice=True)
    price = IntegerField('Price', validators=[DataRequired("This field is required")])
    capacity = IntegerField('Capacity', validators=[DataRequired("This field is required")])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.course = None

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        self.course = Course.find_by_abbr(self.abbreviation.data)
        if not self.course:
            return True

        self.abbreviation.errors.append('Course already exists')
        return False
