from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from app.data.models.user import User
from app.data.models.terms import Term
from app.data.models.news import News
from app.data.models.course import Course
