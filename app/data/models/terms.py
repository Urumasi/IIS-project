from app.data import db
from app.data.mixins import CRUDMixin
import datetime


class Term(db.Model, CRUDMixin):
    name = db.Column(db.String())
    type = db.Column(db.String(length=30))
    description = db.Column(db.String())
    date = db.Column(
        db.DateTime(timezone=True),
        default=datetime.datetime.utcnow
    )
    room = db.Column(db.String())
    rathing = db.Column(db.Integer())
