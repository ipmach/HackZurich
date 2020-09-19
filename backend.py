from flask import Flask
from main import Logic
from flask import request
from markupsafe import escape


app = Flask(__name__)
l = Logic()

@app.route('/alive')
def isAlive():
    return {"State": "200 server alive"}

@app.route('/predict/')
def prediction():
    return l.return_data_ingredients(["Pineapple", "Pepperoni"])
