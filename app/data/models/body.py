from app.data import db


# Gde body
term_body = db.Table('term_body',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('term_id', db.Integer, db.ForeignKey('term.id'), primary_key=True),
                     db.Column('body', db.Integer)
                     )
