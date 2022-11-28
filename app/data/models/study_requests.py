import datetime
from app.data import db
from app.data.mixins import CRUDMixin


class StudyRequest(db.Model, CRUDMixin):
    requester = db.Column(db.Integer(), db.ForeignKey('user.id'))
    course = db.Column(db.Integer(), db.ForeignKey('course.id'))

    created_ts = db.Column(
        db.DateTime(timezone=True),
        default=datetime.datetime.now
    )

    @classmethod
    def find_existing(cls, user, course):
        return StudyRequest.query.filter_by(requester=user.id, course=course.id).first()

    def accept(self):
        from app.data import Course, User
        course = Course.get_by_id(self.course)
        user = User.get_by_id(self.requester)
        course.students.append(user)
        course.save()
        self.delete()

    def reject(self):
        self.delete()

    def get_requester(self):
        from app.data import User
        return User.get_by_id(self.requester)
