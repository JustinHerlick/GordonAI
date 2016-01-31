from yummlyExtractor import YummlyExtractor
import random
import datetime as dt

from flask import (Flask, render_template, redirect,
	url_for, request, make_response,
	flash)

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('form page.html')

@app.route('/main', methods=['POST'])
def main():
   yc = YummlyExtractor()

   ingreds = request.form['ingredients']
   if(ingreds=="e.g. Chicken, Quinoa"):
      ingreds = "Chicken"

   sweetness = float(request.form['sweetness'])
   meatyness = float(request.form['meatyness'])
   saltyness = float(request.form['saltyness'])
   
   name = request.form ['name']
   if(name == "e.g. Ramsay"):
      name = "Ramsay"

   def getMin(number):
      x = 0
      if (number - 10) > 0:
         x = number - 10
      return x/100

   def getMax(number):
      x = 100
      if (number + 10) < 100:
         x = number + 10
      return x/100

   flavors = {
    'sweet': {
        'min': getMin(sweetness),
        'max': getMax(sweetness),
      },
    'meaty': {
        'min': getMin(meatyness),
        'max': getMax(meatyness),
      },
    'bitter': {
        'min': 0,
        'max': 1,
      },
    'salty': {
        'min': getMin(saltyness),
        'max': getMax(saltyness),
      },
    'piquant': {
        'min': 0,
        'max': 1,
      }
   }

   quotes = [
      "\"Until I discovered cooking, I was never really interested in anything.\""
      ,"\"I cook with wine, sometimes I even add it to the food.\""
      ,"\"What are you?\"\n\"An idiot sandwich\""
      ,"\"Cooking is at once child's play and adult joy. And cooking done with care is an act of love.\""
      ,"\"Oh, I adore to cook. It makes me feel so mindless in a worthwhile way.\""
   ]
   
   time = int(request.form['Time'])*60;
   recipes = yc.choose_recipes(ingreds, flavors, time, 5)

   meals = [recipe['name'] for recipe in recipes]
   pictures = [recipe['img'] for recipe in recipes]
   sources = [recipe['src'] for recipe in recipes]
   dates = [(dt.datetime.today() + dt.timedelta(days=i)).strftime('%A') for i in range(5)]

   return render_template('layout.html', meals=meals, pics = pictures, src = sources, name = name, quote = random.choice(quotes), dates=dates)

app.run(debug=True, host='0.0.0.0', port=9110)