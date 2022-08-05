from flask_wtf import FlaskForm
from wtforms import StringField, TimeField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class TaskForm(FlaskForm):
    title = StringField('Name of Song', validators=[DataRequired()])
    artist = StringField('Name of Artist', validators=[DataRequired()])
    # year = SelectField('Year of Release', coerce=int , validators=[DataRequired()])
    # date = DateField('Date of Release', format='%Y-%m-%d' , validators=[DataRequired()])
    # time = TimeField('Time', format='%H:%M' , validators=[DataRequired()])
    submit = SubmitField('Add task')