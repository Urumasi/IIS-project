import datetime
from flask_login import UserMixin
from sqlalchemy import func

from app.data import db, News, Term
from app.data.models.helper_tables import course_students
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
        courses = course_students.query.filter_by(user_id=id).all()
        return {course.course_id: News.get_all_news_for_course(course.course_id) for course in courses}

    def get_all_terms(self):
        courses = course_students.query.filter_by(user_id=id).all()
        return {course.course_id: Term.get_all_terms_for_course(course.course_id) for course in courses}
