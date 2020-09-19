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

@app.route('/co2/<product>')
def product_rating(product):
    #get from data base
    print(l.return_data_CO2(product))
    return l.return_data_CO2(product)

@app.route('/ingredients/<product>')
def ingredient(product):
    #get from data base
    print(l.return_data_pizza(product))

    return l.return_data_pizza(product)

@app.route('/nutrients/<product>')
def getNutrients(product):
    return l.return_nutrients_ingredients(product)

""" Back up functions in case Migros/ IBM fails """

@app.route('/offline_ingredients/<product>')
def ingredient_off(product):
    #get from data base

    return l.return_data_pizza(product)

if __name__ == '__main__':
    app.run(debug=True)
