import yummly
import random
import pprint as pp

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
    'salty': {
        'min': 0,
        'max': 0.75,
    },
    'piquant': {
        'min': 0,
        'max': 0.5,
    }
}

class YummlyExtractor:

    TIMEOUT = 5.0
    RETRIES = 0
    yummly = yummly.Client(api_id="b5d7ae76", api_key="91fa5e6f2cf90d2f2d62494020d6abfa", timeout=TIMEOUT, retries=RETRIES)
    loadedResults = list()
    chosenResults = list()
    processedChosenResults = list()
    recipesYummyFormat = list()
    recipesOurFormat = list()

    def __init__(self):
        x = 1 ## ignore

    def get_recipe_ids(self, ingreds, flavors, time, count):
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
            'flavor.salty.max': flavors['salty']['min'],
            'flavor.salty.max': flavors['salty']['max'],
            'flavor.piquant.min': flavors['piquant']['min'],
            'flavor.piquant.max': flavors['piquant']['max'],
        }
        YummlyExtractor.loadedResults = YummlyExtractor.yummly.search(**params).matches

    def process_recipes(self, recipes):
        return [{'name': recipe.name,
                 'time': recipe.totalTime,
                 'img': recipe.images[0].hostedLargeUrl,
                 'src': recipe.source.sourceRecipeUrl}
                for recipe in recipes]

    def choose_recipes(self, ingreds, flavors, time, count):
        YummlyExtractor.get_recipe_ids(self, ingreds, flavors, time, 100)

        if YummlyExtractor.loadedResults.__len__() < count:
            c = YummlyExtractor.loadedResults.__len__()
        else:
            c = count

        YummlyExtractor.chosenResults = random.sample(YummlyExtractor.loadedResults, c)
        YummlyExtractor.recipesYummyFormat = [YummlyExtractor.yummly.recipe(match.id) for match in YummlyExtractor.chosenResults]
        YummlyExtractor.recipesOurFormat = YummlyExtractor.process_recipes(self, YummlyExtractor.recipesYummyFormat)

        return YummlyExtractor.recipesOurFormat

    def replace_one_recipe(self, itemno):

        overwritten = False

        while overwritten == False:
            overwritten = True
            newrec = random.sample(YummlyExtractor.loadedResults, 1)[0]
            for rec in YummlyExtractor.chosenResults:
                if rec == newrec:
                    overwritten = False

        YummlyExtractor.chosenResults[itemno] = newrec

        YummlyExtractor.recipesYummyFormat = [YummlyExtractor.yummly.recipe(match.id) for match in YummlyExtractor.chosenResults]
        YummlyExtractor.recipesOurFormat = YummlyExtractor.process_recipes(self, YummlyExtractor.recipesYummyFormat)

        return YummlyExtractor.recipesOurFormat


'''
ingreds = ['chicken', 'rice']

maxtime = 3600

samplesize = 5

ye = YummlyExtractor()
ye.choose_recipes(ingreds, flavors, maxtime, samplesize)
pp.pprint(ye.recipesOurFormat)
#print('   ')
ye.replace_one_recipe(2)
pp.pprint(ye.recipesOurFormat)'''