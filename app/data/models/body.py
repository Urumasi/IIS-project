from app.data import db


class TermBody(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    term_id = db.Column('term_id', db.Integer, db.ForeignKey('term.id'), primary_key=True)
    body = db.Column('body', db.Integer)
