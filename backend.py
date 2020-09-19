from flask import Flask, render_template
from main import Logic
from flask import request
from markupsafe import escape


app = Flask(__name__, static_url_path='/static')
l = Logic()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/make_your_own')
def own():
    return render_template('make_your_own.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/webcam')
def webcam():
    return render_template('webcam.html')


@app.route('/alive')
def isAlive():
    return {"State": "200 server alive"}

@app.route('/predict/')
def prediction():
    return l.return_data(["Pineapple", "Pepperoni"])

