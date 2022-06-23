from flask import Flask, redirect, url_for, request
from werkzeug.utils import secure_filename
import os
import robotarium
import robotarium_abc
import numpy as np
import time

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "./static/text"



@app.route('/')
def hello():
    return '<h1>Hello, World</h1>'

@app.route('/simulationVideo',methods = ['POST'])
def login():
    if request.method == 'POST':
        str1 = request.form['code']
        file = open("./static/text/Code.txt", "w")
        fileNum = file.write(str1)
        file.close()
        #if file:
        #    filename = secure_filename(file.filename)
        #    file.save(app.config['UPLOAD_FOLDER'] + "/" + filename)
        #    a = 'file uploaded'
        
        #open text file in read mode
        text_file = open("./static/text/Code.txt", "r")

        #read whole file to a string
        code = text_file.read()
        print(code)
        exec(code,{})
        
        
        return url_for('display_video')

@app.route('/track',methods = ['GET'])
def track():
    if request.method == 'GET':
        time.sleep(1)
        if os.path.isfile('./images/1.png'):
            return '200'
        else:
            return '100'
      

@app.route('/display_video/video.mp4')
def display_video():
	#print('display_video filename: ' + filename)
	return url_for('static', filename='uploads/' + 'video.mp4',code=301)


