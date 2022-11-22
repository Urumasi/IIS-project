from app.data import db, User, News
from app.data.mixins import CRUDMixin

course_students = db.Table('course_students',
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                           db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
                           )

course_lecturers = db.Table('course_lecturers',
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                            db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
                            )


class Course(db.Model, CRUDMixin):
    abbreviation = db.Column(db.String(length=30), nullable=False, unique=True)
    description = db.Column(db.String())
    type = db.Column(db.String())
    price = db.Column(db.Integer())
    capacity = db.Column(db.Integer())
    guarantor = db.Column(db.Integer(), db.ForeignKey('user.id'))

    @classmethod
    def get_all(cls):
        return Course.query.all()

    @classmethod
    def get_all_studied_courses(self, id):
        return Course.query.join(course_students).filter_by(user_id=id).all()

    @classmethod
    def get_all_taught_courses(self, id):
        return Course.query.join(course_lecturers).filter_by(user_id=id).all()

    @classmethod
    def get_all_guaranteed_courses(self, id):
        return Course.query.join(User).filter_by(id = id).all()


    def get_guarantor(self):
        return User.query.join(Course).filter(Course.id == self.id).first()

    def get_all_students(self):
        return User.query.join(course_students).filter_by(course_id=self.id).all()

    def get_all_lecturers(self):
        return User.query.join(course_lecturers).filter_by(course_id=self.id).all()

    def get_all_news(self):
        return News.query.join(Course).filter(Course.id == self.id).all()
