from .core import app, db
from .core.models import Todo
from .core.task.models import Category
from .core.auth.models import User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User,'Todo': Todo, 'Category':Category}