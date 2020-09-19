from flask import Flask, render_template
from main import Logic
from flask import request
from markupsafe import escape
import json

app = Flask(__name__, static_url_path='/static')
l = Logic()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/make_your_own')
def own():
    return render_template('make_your_own.html')

@app.route('/result/<ingredients>')
def result(ingredients):
    ingredients=ingredients.split('&')
    return render_template('result.html', ingredients=ingredients)

@app.route('/webcam')
def webcam():
    return render_template('webcam.html')


@app.route('/alive')
def isAlive():
    return {"State": "200 server alive"}

@app.route('/co2/<product>')
def product_rating(product):
    #get from data base
    return json.dumps(l.return_data_CO2(product))

@app.route('/ingredients/<product>')
def ingredient(product):
    #get from data base
    return json.dumps(l.return_data_pizza(product))



""" Back up functions in case Migros/ IBM fails """

@app.route('/offline_ingredients/<product>')
def ingredient_off(product):
    #get from data base

    return json.dumps(l.return_data_pizza(product))

if __name__ == '__main__':
    app.run(debug=True)