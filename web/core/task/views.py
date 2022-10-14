from flask import render_template, flash, redirect, url_for, request
# from .models import Category
from ..models import Todo
from . import task
from .forms import TaskForm
from .. import db
# from datetime import datetime
from web.config import Configuration
import os
from werkzeug.utils import secure_filename
import librosa
import numpy as np
import os
from flask_login import current_user

# Preprocessing
# from sklearn.preprocessing import StandardScaler

#Keras
from keras import models

import warnings
warnings.filterwarnings('ignore')

genres = np.array('blues classical country disco hiphop jazz metal pop reggae rock'.split())

def genreClassifier():
    songFolder = 'C:\\Users\\urvaa\OneDrive\Desktop\React\\web\\back\\uploads'
    print(songFolder)
    print(os.listdir(f'{songFolder}'))
    for filename in os.listdir(f'{songFolder}'):
        print(filename)
        y, sr = librosa.load(f"{songFolder}\{filename}", mono=True, duration=30)
        print(y)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        rmse = librosa.feature.rms(y=y)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        row = [np.mean(chroma_stft), np.mean(rmse), np.mean(spec_cent), np.mean(spec_bw), np.mean(rolloff), np.mean(zcr)]
        for e in mfcc:
            row.append(np.mean(e))
    X = (np.array(row))[np.newaxis, :]
    model = models.load_model('C:\\Users\\urvaa\OneDrive\Desktop\React\\web\core\\task\model_weights')
    predictions = np.squeeze(model.predict(X))

    model_prediction = np.argmax(predictions)
    return genres[model_prediction]

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
    print(current_user._get_current_object())
    user_id = current_user._get_current_object().id
    todo= Todo.query.filter_by(user_id=user_id)
    print(todo)
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
            print("submit")
            file = form.audiofile.data
            if file.filename == '':
                flash('No file was selected')
                return redirect(request.url)
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(Configuration.UPLOAD_FOLDER, filename))
                genre = genreClassifier()
                print("song created")
                # selected= form.category.data
                # category= Category.query.get(selected)
                todo = Todo(title=form.title.data, genre=genre, artist=form.artist.data, user_id=user_id)
                db.session.add(todo)
                db.session.commit()
                flash('Congratulations, you just added a new note')
                return redirect(url_for('task.tasks'))
            else:
                flash('Allowed media types are - mp3')
                return redirect(request.url)
            
        

    

    return render_template('tasks.html', title='Create Tasks', form=form, todo=todo, check=check)
