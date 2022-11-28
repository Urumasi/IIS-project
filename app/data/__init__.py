from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from app.data.models.user import User
from app.data.models.terms import Term
from app.data.models.news import News
from app.data.models.course import Course, course_lecturers, course_students
from app.data.models.body import TermBody
from app.data.models.course_requests import CourseRequest
from app.data.models.study_requests import StudyRequest
