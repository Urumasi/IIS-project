from app.data import db
from app.data.mixins import CRUDMixin
from sqlalchemy import func

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
    auto_accept_students = db.Column(db.Boolean(), default=False)

    students = db.relationship('User', secondary=course_students)

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
        from app.data import User
        return Course.query.join(User).filter_by(id = id).all()

    def get_guarantor(self):
        from app.data import User
        return User.query.join(Course).filter(Course.id == self.id).first()

    def get_all_students(self):
        from app.data import User
        return User.query.join(course_students).filter_by(course_id=self.id).all()

    def get_all_lecturers(self):
        from app.data import User
        return User.query.join(course_lecturers).filter_by(course_id=self.id).all()

    def get_all_news(self):
        from app.data import News
        return News.query.filter_by(course=self.id).all()

    def get_all_terms(self):
        from app.data import Term
        return Term.query.filter_by(course=self.id).all()

    @staticmethod
    def exists(abbreviation):
        from app.data import Course
        if Course.find_by_abbr(abbreviation):
            return True
        return False

    @staticmethod
    def find_by_abbr(abbreviation):
        from app.data import Course
        return Course.query.filter(Course.abbreviation == abbreviation).first()

    def is_taught_by(self, user):
        if user.id == self.guarantor:
            return True
        lecturers = self.get_all_lecturers()
        return any(user.id == lecturer.id for lecturer in lecturers)

    def is_studied_by(self, user):
        students = self.get_all_students()
        return any(user.id == student.id for student in students)
