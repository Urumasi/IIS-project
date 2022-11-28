from app.data import db


class TermBody(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    term_id = db.Column('term_id', db.Integer, db.ForeignKey('term.id'), primary_key=True)
    body = db.Column('body', db.Integer)

    @classmethod
    def get_by_ids(cls, user_id, term_id):
        return TermBody.query.filter_by(user_id=user_id, term_id=term_id).first()

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self
