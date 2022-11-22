from app.data import db
from app.data.mixins import CRUDMixin


class News(db.model, CRUDMixin):
    course = db.Column(db.Integer, db.ForeignKey('course.id'))
    da_newz = db.Column(db.String())
