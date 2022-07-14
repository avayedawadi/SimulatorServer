#Ubuntu
from flask import Flask, redirect, url_for, request, send_from_directory
from werkzeug.utils import secure_filename
import os
import robotarium
import robotarium_abc
import numpy as np
import time
import threading
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = "rps/static/text"

# my background thread
class MyWorker():

    def __init__(self, message):
        self.message = message

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):

        # do something
        text_file = open("rps/static/text/Code.txt", "r")

        #read whole file to a string
        code = text_file.read()
        print(code)
        exec(code,{})


@app.route('/')
def hello():
    return '<h1>Hello, World</h1>'

@app.route('/static/<path:path>')
def send_report(path):
    return send_from_directory('static', path)


@app.route('/simulationVideo',methods = ['POST'])
def login():
    if request.method == 'POST':
        code = request.form['code']
        #file = open("./static/text/Code.txt", "w")
        #fileNum = file.write(str1)
        #file.close()
        #if file:
        #    filename = secure_filename(file.filename)
        #    file.save(app.config['UPLOAD_FOLDER'] + "/" + filename)
        #    a = 'file uploaded'
        
        #open text file in read mode
        
        #MyWorker('test')
        
             

        localDict = {}
        exec(code,{})
        timetamp = ""
        with open('rps/static/text/timestamp.txt') as f:
            timestamp = f.readlines()[0]
        
        #return url_for('display_video')
        return timestamp

@app.route('/track',methods = ['GET'])
def track():
    if request.method == 'GET':
        time.sleep(1)
        if os.path.isfile('rps/images/1.png'):
            return '200'
        else:
            return '100'
      

@app.route('/display_video/video.mp4')
def display_video():
	#print('display_video filename: ' + filename)
	return url_for('static', filename='uploads/' + 'video.mp4',code=301)

if __name__ == "__main__":
    app.run(debug=True)


