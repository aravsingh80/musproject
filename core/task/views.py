from flask import render_template, flash, redirect, url_for, request
from .models import Category
from ..models import Todo
from . import task
from .forms import TaskForm
from .. import db
from datetime import datetime
from config import Configuration
import os
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Configuration.ALLOWED_EXTENSIONS

@task.route('/create-task', methods=['GET', 'POST'])
def tasks():
    check= None
    # date= datetime.now()
    # now= date.strftime("%Y-%m-%d")

    # categories = [Category(name="Business"), Category(name="Personal"), Category(name="Other")]
    # for c in categories:
    #     db.session.add(c)
    # db.session.commit()
    
    form= TaskForm()
    # form.category.choices =[(category.id, category.name) for category in Category.query.all()]
    todo= Todo.query.all()
    if request.method == "POST":
        print("Inside post")
        if request.form.get('taskDelete') is not None:
            print("Inside task delete branch")
            print(request.form)
            deleteTask = request.form.get('checkedbox')
            if deleteTask is not None:
                print("Inside task delete branch 2")
                todo = Todo.query.filter_by(id=int(deleteTask)).one()
                db.session.delete(todo)
                db.session.commit()
                return redirect(url_for('task.tasks'))
            else:
                check = 'Please check-box of task to be deleted'

        elif form.validate_on_submit():
            print("song created")
            # selected= form.category.data
            # category= Category.query.get(selected)
            todo = Todo(title=form.title.data, artist=form.artist.data)
            db.session.add(todo)
            db.session.commit()
            flash('Congratulations, you just added a new note')
            return redirect(url_for('task.tasks'))
        

        file = request.files['file']
        if file.filename == '':
            flash('No file was selected')
            return redirect(request.url)
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(Configuration.UPLOAD_FOLDER, filename))
            flash('File has been successfully uploaded')
            return redirect('/create-task')
        else:
            flash('Allowed media types are - mp3')
            return redirect(request.url)

    return render_template('tasks.html', title='Create Tasks', form=form, todo=todo, check=check)
