from flask_wtf import FlaskForm
from wtforms import StringField, TimeField, DateField, SubmitField, SelectField, FileField
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask import Flask
from config import Configuration
app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __repr__(self):
        return '<Category {}>'.format(self.name)

class TaskForm(FlaskForm):
    title = StringField('Name of Song', validators=[DataRequired()])
    artist = StringField('Name of Artist', validators=[DataRequired()])
    audiofile = FileField()
    submit = SubmitField('Add task')
