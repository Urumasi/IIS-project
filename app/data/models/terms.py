from app.data import db, Course
from app.data.mixins import CRUDMixin
import datetime


class Term(db.Model, CRUDMixin):
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    name = db.Column(db.String())
    type = db.Column(db.String(length=30))
    description = db.Column(db.String())
    date = db.Column(
        db.DateTime(timezone=True),
        default=datetime.datetime.utcnow
    )
    room = db.Column(db.String())
    rathing = db.Column(db.Integer())

    @classmethod
    def get_all_terms_for_course(cls, course_id):
        return Term.query.filter(course=course_id).all()

    @classmethod
    def get_all_terms_for_user(cls, user_id):
        courses = Course.get_all_studied_courses(user_id)
        return {course: Term.get_all_news_for_course(course) for course in courses}

