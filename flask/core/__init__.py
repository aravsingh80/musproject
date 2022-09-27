from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login'

from core import views, models

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .task import task as task_blueprint
app.register_blueprint(task_blueprint)