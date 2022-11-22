from app.data import db
from app.data.mixins import CRUDMixin

course_students = db.Table('course_students',
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                           db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
                           )

course_lecturers = db.Table('course_lecturers',
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                            db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
                            )


class Course(db.model, CRUDMixin):
    abbreviation = db.Column(db.String(length=30), nullable=False, unique=True)
    description = db.Column(db.String())
    type = db.Column(db.String())
    price = db.Column(db.Integer())
    capacity = db.Column(db.Integer())
    guarantor = db.Column(db.ForeignKey())
