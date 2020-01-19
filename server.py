from flask import Flask, request, render_template, redirect
import os, subprocess, time
import TranscriptGeneration.adafruitmetrics as adafruit
from TranscriptGeneration.transcriptcreate import transcript_gen,send_email

app = Flask(__name__)

@app.route('/stop')
def stop():
    os.system("python publish.py")
    return render_template("STOP.html")

@app.route('/start')
def start():
    os.system("python stopublish.py")
    print("generating transcript")
    global blood_pressure, heart_rate
    # metrics = os.system("python TranscriptGeneration/transcript_create.py")
    time.sleep(15)
    metrics = transcript_gen()
    print(type(metrics), len(metrics))
    blood_pressure = str(metrics[0])
    heart_rate = str(metrics[1])
    print("done generating transcript")
    print("sending email")
    send_email()
    print("sent email")
    return render_template("START.html")

@app.route('/metrics')
def metrics():
    #adafruit.main(0, blood_pressure)
    return redirect("https://io.adafruit.com/vishakh_arora29/dashboards/dvhacks-metrics?kiosk=true")

@app.route('/transcript')
def transcript():
    fin = open("transcript.txt","r")
    return fin.read()


@app.route('/')
def index():
    return render_template("START.html")

if __name__ == "__main__":
    app.run(debug=True)
