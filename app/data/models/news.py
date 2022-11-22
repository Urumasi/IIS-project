from app.data import db, Course
from app.data.mixins import CRUDMixin


class News(db.Model, CRUDMixin):
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    da_newz = db.Column(db.String())

    @classmethod
    def get_all_news_for_course(cls, course_id):
        return News.query.filter(course=course_id).all()

    @classmethod
    def get_all_news_for_user(cls, user_id):
        courses = Course.get_all_studied_courses(user_id)
        return {course: News.get_all_news_for_course(course) for course in courses}
