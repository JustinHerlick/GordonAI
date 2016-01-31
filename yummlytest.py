from __future__ import print_function
import yummly
import random
import pprint
import sys

TIMEOUT = 5.0
RETRIES = 0

yummly = yummly.Client(api_id="b5d7ae76", api_key="91fa5e6f2cf90d2f2d62494020d6abfa", timeout=TIMEOUT, retries=RETRIES)

flavors = {
    'sweet': {
        'min': 0,
        'max': 0.75,
    },
    'meaty': {
        'min': 0,
        'max': 1,
    },
    'bitter': {
        'min': 0,
        'max': 0.25,
    },
    'piquant': {
        'min': 0,
        'max': 0.5,
    }
}

ingreds = ['chicken', 'rice']

def get_recipe_ids(ingreds, flavors, time, count):
    
    params = {
        'q': ingreds,
        'start': 0,
        'requirePictures': True,
        'maxResult': count,
        'maxTotalTimeInSeconds': time,
        'flavor.sweet.min': flavors['sweet']['min'],
        'flavor.sweet.max': flavors['sweet']['max'],
        'flavor.meaty.min': flavors['meaty']['min'],
        'flavor.meaty.max': flavors['meaty']['max'],
        'flavor.bitter.min': flavors['bitter']['min'],
        'flavor.bitter.max': flavors['bitter']['max'],
        'flavor.piquant.min': flavors['piquant']['min'],
        'flavor.piquant.max': flavors['piquant']['max'],
    }
    results = yummly.search(**params).matches
    return results

def process_recipes(recipes):
    return [{'name': recipe.name,
             'time': recipe.totalTime,
             'img': recipe.images[0].hostedLargeUrl}
            for recipe in recipes]

def choose_recipes(ingreds, flavors, time, count):
    results = get_recipe_ids(ingreds, flavors, time, count)
    
    print(ingreds, file=sys.stderr)
    
    chosen = random.sample(results, count)
    recipes = [yummly.recipe(match.id) for match in chosen]
    return process_recipes(recipes)
 
 #pprint.pprint(choose_recipes(ingreds, flavors, 3600, 5)) 