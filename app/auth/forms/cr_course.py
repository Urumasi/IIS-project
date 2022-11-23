from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from app.data import Course


class CreateCourseForm(FlaskForm):
    abbreviation = StringField('Abbreviation', validators=[DataRequired("This field is required"), Length(min=3, max=5,
                                                                                                          message="Abbr"
                                                                                                                  "evia"
                                                                                                                  "tion"
                                                                                                                  " sho"
                                                                                                                  "uld "
                                                                                                                  "be b"
                                                                                                                  "etwe"
                                                                                                                  "en 3"
                                                                                                                  " and"
                                                                                                                  " 5 c"
                                                                                                                  "hara"
                                                                                                                  "cter"
                                                                                                                  "s lo"
                                                                                                                  "ng!"
                                                                                                          )])
    description = StringField('Description', validators=[DataRequired("This field is required")])
    type = RadioField('Select type', validators=[DataRequired("This field is required")],
                      choices=[('in-person', 'In-person'), ('distance', 'Distance')])
    price = IntegerField('Price',
                         validators=[DataRequired("This field is required"), NumberRange(min=0, max=2 ** 31 - 1,
                                                                                         message="Don't "
                                                                                                 "overflow "
                                                                                                 "the "
                                                                                                 "database "
                                                                                                 "please")])
    capacity = IntegerField('Capacity', validators=[DataRequired("This field is required"), NumberRange(min=10,
                                                                                                        max=2 ** 31 - 1,
                                                                                                        message="Don'"
                                                                                                                "t "
                                                                                                                "over"
                                                                                                                "flow"
                                                                                                                " "
                                                                                                                "the "
                                                                                                                "data"
                                                                                                                "base"
                                                                                                                " "
                                                                                                                "plea"
                                                                                                                "se"
                                                                                                        )])

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
