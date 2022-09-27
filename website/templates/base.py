from flask import Flask
from flask import render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, TimeField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import datetime
import os
from dotenv import load_dotenv 

app = Flask(__name__)

@app.route("/members")
def members():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)