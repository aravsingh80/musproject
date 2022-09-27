from core import db
from datetime import datetime

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    genre = db.Column(db.String(140))
    # date = db.Column(db.Date())
    # time = db.Column(db.Time())
    artist= db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<ToDo {}>'.format(self.title)