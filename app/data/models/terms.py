from app.data import db
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
    max_body = db.Column(db.Integer())

    def get_body(self, user):
        from app.data import term_body
        result = term_body.query.filter_by(user_id=user.id, term_id=self.id).first()
        return result.body if result else None
