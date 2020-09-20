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
    ingredients1=ingredients.split('&')[1:]
    try:
        co2=l.return_data_CO2(ingredients.split('&')[0])["recipe"]["rating"]
    except:
        co2="Not found"
    return render_template('result.html', ingredients=ingredients1, co2=co2)

@app.route('/data/<ingredient>')
def data(ingredient):
    ingredient=ingredient
    nutrition= l.return_nutrients_ingredients(ingredient)
    #print(co2)
    print(nutrition)
    return render_template('data.html', ingredient=ingredient, nutrition=nutrition)

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
    response=json.dumps(l.return_data_pizza(product))
    print(response)
    return response

@app.route('/nutrients/<product>')
def getNutrients(product):
    return json.dumps(l.return_nutrients_ingredients(product))

""" Back up functions in case Migros/ IBM fails """

@app.route('/offline_ingredients/<product>')
def ingredient_off(product):
    #get from data base

    return json.dumps(l.return_data_pizza(product))

if __name__ == '__main__':
    app.run(debug=True)
