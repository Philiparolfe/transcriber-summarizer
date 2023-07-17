from flask import Flask, render_template, request, redirect
#GUI
from flaskwebgui import FlaskUI

import recorder as r
import whisper_module as wspr
from time import sleep
import os
import gpt_extractor as gpt
import datetime



app = Flask(__name__)


TRANS = '' 


# @app.route("/", methods=['GET', 'POST'])
# def index():
#     # os.remove("output.wav")
#     return render_template('index.html')

@app.route("/new", methods=['GET', 'POST'])
def new():
    global TRANS
    TRANS = ''
    if os.path.exists("output.wav"):
        os.remove("output.wav")
    return index()
#python record (server side)
@app.route("/recording", methods=['GET', 'POST'])
def recording():
    r.STATUS = True
    r.record_audio()
    return index()

#javascript record (client side)
@app.route("/")
def index():
    return render_template("record.html")

@app.route("/stopped", methods=['GET', 'POST'])
def stop_recording():
    
    r.STATUS = False
    sleep(3.0)
    return redirect("/transcribe", code=302)


@app.route("/transcribe", methods=['GET', 'POST'])
def get_transcription():
    try:
        text = wspr.whisper_transcribe('output.wav')
        global TRANS
        TRANS = text
        return render_template('transcript.html', text=text)
    except Exception as err:
        print(f"{err}")
        return render_template('transcript.html', text="Error")
       
def log_to_file(log_string, file_path):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"log_{timestamp}.txt"
    file_path_with_name = os.path.join(file_path, file_name)
    
    # Create directory if it doesn't exist
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    
    with open(file_path_with_name, 'a') as file:
        file.write(log_string + '\n')
@app.route("/extract", methods=['GET', 'POST'])
def get_extraction():
    
    try:
        
        text = gpt.extract(TRANS)
        log_to_file(str(text), "logs/")
        return render_template('extracted.html', text=text)
    except Exception as err:
        print(f"{err}")
        log_to_file("Error.", "logs/")
        return render_template('transcript.html', text="Error")

@app.route("/upload", methods=['POST'])
def upload():
    audio = request.files['audio']
    audio.save('output.wav')
    return 'Audio uploaded successfully'

@app.route("/status", methods=['GET'])
def status():
    return f"{r.STATUS}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
   
    #FlaskUI(app=app, server="flask").run()