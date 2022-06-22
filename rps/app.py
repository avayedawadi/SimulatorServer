from flask import Flask, redirect, url_for, request
from werkzeug.utils import secure_filename
import os
import robotarium
import robotarium_abc
import numpy as np

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "rps/static/text"



@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/simulationVideo',methods = ['POST'])
def login():
   if request.method == 'POST':
        file = request.files['code']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            a = 'file uploaded'
        
        #open text file in read mode
        text_file = open("rps/static/text/Code.txt", "r")

        #read whole file to a string
        code = text_file.read()
        print(code)
        exec(code,{})
        
        
        return url_for('display_video')
      

@app.route('/display_video/video.mp4')
def display_video():
	#print('display_video filename: ' + filename)
	return url_for('static', filename='uploads/' + 'video.mp4',code=301)

