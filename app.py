from flask import Flask, render_template, request, redirect
import recorder as r
import whisper_module as wspr
from time import sleep
import os
import gpt_extractor as gpt



app = Flask(__name__)



@app.route("/", methods=['GET', 'POST'])
def index():
    # os.remove("output.wav")
    return render_template('index.html')

@app.route("/new", methods=['GET', 'POST'])
def new():
    if os.path.exists("output.wav"):
        os.remove("output.wav")
    return index()

@app.route("/recording", methods=['GET', 'POST'])
def recording():
    r.STATUS = True
    r.record_audio()
    return index()

@app.route("/stopped", methods=['GET', 'POST'])
def stop_recording():
    
    r.STATUS = False
    sleep(3.0)
    return redirect("/transcribe", code=302)

@app.route("/transcribe", methods=['GET', 'POST'])
def get_transcription():
    try:
        text = wspr.whisper_transcribe('output.wav')
        return render_template('transcript.html', text=text)
    except Exception as err:
        print(f"{err}")
        return render_template('transcript.html', text="Error")
        
@app.route("/extract", methods=['GET', 'POST'])
def get_extraction():
    try:
        trans = wspr.whisper_transcribe('output.wav')
        text = gpt.extract(trans)
        return render_template('transcript.html', text=text)
    except Exception as err:
        print(f"{err}")
        return render_template('transcript.html', text="Error")

@app.route("/status", methods=['GET'])
def status():
    return f"{r.STATUS}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)