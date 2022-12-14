import datetime
from flask_login import UserMixin
from sqlalchemy import func

from app.data import db
from app.data.mixins import CRUDMixin
from app.extensions import bcrypt


class User(db.Model, CRUDMixin, UserMixin):
    username = db.Column(db.String(32), nullable=False)
    pw_hash = db.Column(db.String(256), nullable=False)
    created_ts = db.Column(
        db.DateTime(timezone=True),
        default=datetime.datetime.utcnow
    )
    is_active = db.Column(db.Boolean(), default=True)
    is_admin = db.Column(db.Boolean())

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def __repr__(self):
        return f'<User #{self.id}:{self.username}>'

    def set_password(self, password):
        self.pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.pw_hash, password.encode('utf-8'))

    @staticmethod
    def exists(username):
        if User.find_by_name(username):
            return True
        return False

    @staticmethod
    def find_by_name(username):
        return User.query.filter(func.lower(User.username) == func.lower(username)).first()

    def get_all_news(self):
        from app.data import Course
        courses = set()
        courses |= set(Course.get_all_studied_courses(self.id))
        courses |= set(Course.get_all_taught_courses(self.id))
        courses |= set(Course.get_all_guaranteed_courses(self.id))
        return {course: course.get_all_news() for course in courses}

    def get_all_terms(self):
        from app.data import Course
        courses = Course.get_all_studied_courses(self.id)
        return {course: course.get_all_terms() for course in courses}

    def get_body_for_course(self, course):
        terms = course.get_all_terms()
        return sum(filter(None, (term.get_body(self) for term in terms)))
