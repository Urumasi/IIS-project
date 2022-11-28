import datetime
from app.data import db
from app.data.mixins import CRUDMixin


class CourseRequest(db.Model, CRUDMixin):
    requester = db.Column(db.Integer(), db.ForeignKey('user.id'))

    abbreviation = db.Column(db.String(length=30), nullable=False, unique=True)
    description = db.Column(db.String())
    type = db.Column(db.String())
    price = db.Column(db.Integer())
    capacity = db.Column(db.Integer())

    created_ts = db.Column(
        db.DateTime(timezone=True),
        default=datetime.datetime.now
    )

    def accept(self):
        from app.data import Course
        Course.create(
            abbreviation=self.abbreviation,
            description=self.description,
            type=self.type,
            price=self.price,
            capacity=self.capacity,
            guarantor=self.requester
        )
        self.delete()

    def reject(self):
        self.delete()
