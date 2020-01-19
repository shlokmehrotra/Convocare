from flask import Flask, request, render_template, redirect
import os, subprocess, time
import TranscriptGeneration.adafruitmetrics as adafruit
from TranscriptGeneration.transcriptcreate import transcript_gen,send_email

app = Flask(__name__)

@app.route('/stop')
def stop():
    # mosquitto_pub -d -t omnihacks -m \"record\"
    os.system("python publish.py")
    return render_template("STOP.html")
