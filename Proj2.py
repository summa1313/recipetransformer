# -*- coding: utf-8 -*-
import re
import scrapeRecipe as scraper
import parseRecipe as parser
from kb import *

#url = input('Please enter a recipe url from AllRecipes.com: ')
#recipe = scraper.scrapeRecipe(url)

#recipe = scraper.scrapeRecipe(
#    'https://www.allrecipes.com/recipe/73634/colleens-slow-cooker-jambalaya/?internalSource=previously%20viewed&referringContentType=home%20page&clickId=cardslot%204')
#recipe['ingredients'] = parser.parseIngredients(recipe['ingredients'])

#recipe['directions'] = parser.parseDirections(recipe['directions'], recipe['ingredients'])
# print (recipe['directions'])

#chnage ml to l where needed in output and g to kg


#!! This two functions can be used for our output (need to add option selection) !!
def formatQuantity(quantity, unitSystem):
    """
    Converts quatntity into human-readable string depending on unit system
    """
    # if integer
    if int(quantity) == quantity:
        return str(int(quantity))
    # has fractions
    if unitSystem == 'american':
        fraction = quantity - int(quantity)
        for i in range(1,9):
            for j in range(1, 9):
                if fraction == i/j:
                    result = ''
                    if quantity > 1:
                        result += str(int(quantity)) + ' '
                    result += str(i) + '/' + str(j)
                    return result
        return str(int(quantity))
    return str(quantity)

def printRecipe(recipe):
    """
    Prints recipe
    """
    unitSystem = checkUnitSystem(recipe)
    print('--------------------------')
    print(recipe['recipeName'])
    print('\nIngredients:')
    for t in recipe['ingredients']:
        q = formatQuantity(t['quantity'], unitSystem)
        q = q + ' ' + t['unit'] if t['unit'] != 'N/A' else q
        q = q if t['quantity'] != -1 else ''
        if 'subUnit' in t and t['subUnit'] != 'N/A' and unitSystem == 'american':
            q = q + " (" + str(t['subQuantity']) + ' ' + t['subUnit'] + ')'
        q = q + ' ' + t['name']
        if 'descriptors' in t and t['descriptors']:
            q = q + ', ' + " ".join(t['descriptors'])
        if 'descriptor' in t and t['descriptor']:
            q = q + ", " + t['descriptor']
        print("\t", q)
    print('\nDirections:')
    for t in recipe['directions']:
        print(t[0].capitalize())


def checkUnitSystem(recipe):
    for i in recipe['ingredients']:
        if i['unit'] in unitTable or i['unit'] == 'pound' or i['unit'] == 'can':
            return ('american')
    return ('metric')


# Metric Systems: liters, milliliters, grams, kilograms, degrees Celsius
# USA system: tablespoons, teaspoons, fluid oz, cups, quarts, gallons
def changeUnits(recipe): #Tested->works good
    system = checkUnitSystem(recipe)
    if system == 'american':
        for i in recipe['ingredients']:
            if i['unit'] != 'N/A':
                if 'can' in i['unit']:
                    i['unit'] = 'can'
                if i['unit'] in unconvertibleUnits:
                    if (i['subQuantity'] != -1 and i['subUnit'] != 'N/A'):
                        i['quantity'] = i['subQuantity'] * i['quantity']
                        i['unit'] = i['subUnit']
                    else:
                        continue
                # check if unit of weight
                if i['unit'] == 'lb' or i['unit'] == 'pound':
                    i['quantity'] = i['quantity'] * 450
             #       if i['quantity'] < 1000:
                    i['unit'] = 'g'
              #      else:
              #          i['quantity'] = i['quantity'] / 1000
               #         i['unit'] = 'kg'
                else:
                    if 'ounce' in i['unit']:
                        i['unit'] = 'oz'
                    i['quantity'] = unitTable[i['unit']] * i['quantity']
               #     if i['quantity'] < 1000:
                    i['unit'] = 'ml'
               #     else:
                #        i['quantity'] = i['quantity'] / 1000
                 #       i['unit'] = 'l'
    # if converting to US system
    elif system == 'metric':
        for i in recipe['ingredients']:
            if i['unit'] != 'N/A' and i['unit'] not in unconvertibleUnits:
                if i['unit'] == 'g':
                    i['quantity'] = i['quantity'] / 450
                    i['unit'] = 'lb'
               # elif i['unit'] == 'kg':
                #    i['quantity'] = i['quantity'] * 1000 / 450
                 #   i['unit'] = 'lb'
                else:
#unitTable = {'gallon': 3785, 'quart': 950, 'pint': 475, 'cup': 240, 'oz': 30, 'tablespoon': 15, 'teaspoon': 5}
                    if (i['quantity'] % 60 == 0 or i['quantity'] % 80 ==0):
                                i['quantity'] = i['quantity'] / unitTable['cup']
                                i['unit'] = 'cup'
                    if i['unit'] == 'ml':
                        for key, value in unitTable.items():
                            if key == 'oz':
                                continue
                            if (i['quantity'] % value == 0):
                                i['quantity'] = i['quantity'] / value
                                i['unit'] = key
                                break
                    if i['unit'] == 'ml':
                        if i['quantity'] % 7.5 == 0:
                                i['quantity'] = i['quantity'] / unitTable['tablespoon']
                                i['unit'] = 'tablespoon'
                        elif (i['quantity'] % unitTable['teaspoon'] == (1/4)*unitTable['teaspoon'] or i['quantity'] % unitTable['teaspoon'] 
                                == (1/3)*unitTable['teaspoon']):
                                i['quantity'] = i['quantity'] / unitTable['teaspoon']
                                i['unit'] = 'teaspoon'
                        else:
                            if i['quantity'] > 5:
                                i['quantity'] = i['quantity'] / unitTable['oz']
                                i['unit'] = 'oz'
                            else:
                                i['quantity'] = i['quantity'] / unitTable['teaspoon']
                                i['unit'] = 'teaspoon'
                    if i['quantity'] > 10 and i['subUnit'] != 'N/A' and i['subQuantity'] != -1:
                                    i['quantity'] = i['subQuantity']
                                    i['unit'] = i['subUnit']
                                    i['subUnit'] = 'N/A'
                                    i['subQuantity'] = -1
                    else:
                        if not (i['unit'] == 'teaspoon' and i['quantity'] <=5 ) and not ( i['unit'] == 'cup' and i['quantity'] <=5 )  and not ( i['unit'] == 'tablespoon' and i['quantity'] <=5 ) :
                            i['quantity'] = i['quantity'] * unitTable[i['unit']] / unitTable['oz']
                            i['unit'] = 'oz'

#printRecipe(recipe)
# do not remove this. all units convert to metric. call function again before output
#changeUnits(recipe)


# checks if animal protein, substitutes with vegetarian.
def toVegetarian(recipe): #works fine
    #change recipe name
    recipe['recipeName'] = 'Vegetarian ' + recipe['recipeName'] 
    #substitute ingredients
    for t in recipe['ingredients']:
        for key in vegetarian_substitutes:
            if key in t['name']:
                t['name'] = vegetarian_substitutes[key]
                break
    
    # make changes in directions.
    for i in range(0, len(recipe['directions'])):
        for key, value in vegetarian_substitutes.items():
            recipe['directions'][i] = (re.sub(key, value, recipe['directions'][i][0]), recipe['directions'][i][1])
        recipe['directions'][i] = (re.sub('(,|and|\.) [a-zA-Z1-9 \/]*breast([a-zA-Z 1-9\/]*)?.', '.', recipe['directions'][i][0]), recipe['directions'][i][1])
        recipe['directions'][i] = (re.sub('(,|and|\.) [a-zA-Z1-9 \/]*bone([a-zA-Z 1-9\/]*)?.', '.', recipe['directions'][i][0]), recipe['directions'][i][1])
        recipe['directions'][i] = (re.sub('(,|and|\.) [a-zA-Z1-9 \/]*skin([a-zA-Z 1-9\/]*)?.', '.', recipe['directions'][i][0]), recipe['directions'][i][1])
        recipe['directions'][i] = (re.sub('(,|and|\.) [a-zA-Z1-9 \/]*cavity([a-zA-Z 1-9\/]*)?.', '.', recipe['directions'][i][0]), recipe['directions'][i][1])
        recipe['directions'][i] = (re.sub('(,|and|\.) [a-zA-Z1-9 \/]*leg([a-zA-Z 1-9\/]*)?.', '.', recipe['directions'][i][0]), recipe['directions'][i][1])
        recipe['directions'][i] = (re.sub('(,|and|\.) [a-zA-Z1-9 \/]*head([a-zA-Z 1-9\/]*)?.', '.', recipe['directions'][i][0]), recipe['directions'][i][1])
        recipe['directions'][i] = (re.sub('carve', 'dice', recipe['directions'][i][0]), recipe['directions'][i][1])
        recipe['directions'][i] = (re.sub(' fillets', '', recipe['directions'][i][0]), recipe['directions'][i][1])
        recipe['directions'][i] = (re.sub('breasts?', '', recipe['directions'][i][0]), recipe['directions'][i][1])


def toNonVegetarian(recipe):
    counter = 0
    #change recipe name
    if 'Vegetarian' in recipe['recipeName']:
        recipe['recipeName'] = re.sub('Vegetarian ', '', recipe['recipeName'])
    if 'Vegan' in recipe['recipeName']:
        recipe['recipeName'] = recipe['recipeName'].replace('Vegan ', '')
    if 'Meatless' in recipe['recipeName']:
        recipe['recipeName'] = re.sub('Meatless ', '', recipe['recipeName'])

    for t in recipe['ingredients']:
        for key, value in vegetarian_substitutes.items():
            if t['name'] == value:
                t['name'] = key
                counter = counter + 1
                break
        for key, value in vegan_substitutes.items():
            if t['name'] == value:
                t['name'] = key
                break
    #if no substitutions in ingredients were made, add chicken
    if counter == 0 and not ifDessert(recipe): 
        ingredient = dict()
        ingredient['name'] = 'chicken breast'
        ingredient['descriptor'] = 'cooked shredded'
        ingredient['quantity'] = 1
        ingredient['unit'] = 'N/A'
        ingredient['subUnit'] = 'N/A'
        ingredient['subQuantity'] = -1
        recipe['ingredients'].append(ingredient)

    # make changes in directions.
    for i in range(0, len(recipe['directions'])):
        for key, value in vegetarian_substitutes.items():
            if value and value in recipe['directions'][i][0]:
                recipe['directions'][i] = (re.sub(value, key, recipe['directions'][i][0]), recipe['directions'][i][1])
        for key, value in vegan_substitutes.items():
            if value and value in recipe['directions'][i][0]:
                recipe['directions'][i] = (re.sub(value, key, recipe['directions'][i][0]), recipe['directions'][i][1])
        recipe['directions'][i] = (re.sub('vegan ', '', recipe['directions'][i][0]), recipe['directions'][i][1])
        recipe['directions'][i] = (re.sub('vegetrian ', '', recipe['directions'][i][0]), recipe['directions'][i][1])

    if counter == 0 and not ifDessert(recipe): 
        recipe['directions'].append(('Serve with chicken.', {}))


# checks if animal protein or eggs or diary, substitutes with vegan.
def toVegan(recipe): #works fine
    #copy names of cheeses if need to substitute all with 1 vegan equivalent
    cheesses = []
    for t in recipe['ingredients']:
    # count nr of cheeses
        if ('cheese' in t['name'] or 'parmesan' in t['name'] or 'mozzarella' in t['name'] or 'Parmesan' in t['name']):
            if t['unit'] != 'N/A':
                cheesses.append(t)
        
        #substitute nonvegan products
        for key in vegan_substitutes:
            if key in t['name']:
                t['name'] = vegan_substitutes[key]
                break
     
     #substitute cheeses with one option
    if len(cheesses) > 1:
        # combine several cheeses into one
        cheesses[0]['subQuantity'] = -1
        cheesses[0]['subUnit'] = 'N/A'
        for i in range(1, len(cheesses)):
            cheesses[0]['quantity'] = cheesses[0]['quantity'] + cheesses[i]['quantity']
            recipe['ingredients'].remove(cheesses[i])

    # make changes in directions.
    for i in range(0, len(recipe['directions'])):
        for key, value in vegan_substitutes.items():
            recipe['directions'][i] = (re.sub(key, value, recipe['directions'][i][0]), recipe['directions'][i][1])
        recipe['directions'][i] = (re.sub('soy soy ', 'soy ', recipe['directions'][i][0]), recipe['directions'][i][1])
        recipe['directions'][i] = (re.sub('vegan soy ', 'vegan ', recipe['directions'][i][0]), recipe['directions'][i][1])
        recipe['directions'][i] = (re.sub('vegan cheese soy ', 'vegan ', recipe['directions'][i][0]), recipe['directions'][i][1])

    toVegetarian(recipe)
    #change recipe name
    recipe['recipeName'] = re.sub('Vegetarian', 'Vegan', recipe['recipeName'])
    
   

# Healthy ->reduce fat, salt, sugar and milk fats, mayonnaise to 50% in ingredient list.
def toHealthy(recipe):
    #change recipe name
    if 'Fatty And Tasty ' in recipe['recipeName']:
        recipe['recipeName'] = re.sub('Fatty And Tasty ', '', recipe['recipeName'])
    recipe['recipeName'] = 'Healthy ' + recipe['recipeName']

    #reduce fats
    for x in recipe['ingredients']:
        for t in fats:
            temp = re.search(t, x['name'])
            if temp:
                x['quantity'] = x['quantity'] * 0.5
                break
    #reduce salt and sugar
        if (x['name'] == 'salt' or 'sugar' in x['name']):
            x['quantity'] = x['quantity'] * 0.5
    # vegetable oil instead of pork fat
        if 'pork fat' in x['name']:
            x['name'] = 'vegetable oil'
    # reduce cheese, whipped cream, sour cream, mayonnaise
        temp = re.search('cheese', x['name'])
        temp2 = re.search('cream', x['name'])
        temp3 = re.search('mayonnaise', x['name'])
        if temp or temp2 or temp3:
            x['quantity'] = x['quantity'] / 2
        # make changes in directions.
    for i in range(0, len(recipe['directions'])):
        recipe['directions'][i] = (re.sub('in pork fat', 'in oil', recipe['directions'][i][0]), recipe['directions'][i][1])
        recipe['directions'][i] = (re.sub('pork fat', 'vegetable oil', recipe['directions'][i][0]), recipe['directions'][i][1])

def toUnhealthy(recipe):
    #change recipe name
    recipe['recipeName'] = re.sub('Healthy ', '', recipe['recipeName'])
    recipe['recipeName'] = 'Fatty And Tasty ' + recipe['recipeName'] 
    counter = 0
    for t in recipe['ingredients']:
        # double cheese, whipped cream, sour cream, mayonnaise
        if 'cheese' in t['name'] or 'cream' in t['name'] or 'mayonnaise' in t['name']:
            t['quantity'] = t['quantity'] * 2
            counter = counter + 1 #checking if unhealthy products in recipe
        # whole milk
        if t['name'] == 'milk':
            t['name'] = 'whole milk'
            counter = counter + 1
        # double fats
        for x in fats:
            temp = re.search(x, t['name'])
            if temp:
                t['quantity'] = t['quantity'] * 2
                counter = counter + 1
                break
        # pork fat instead of vegetable oil
        if ' oil' in t['name']:
            t['name'] = 'pork fat'
        # double salt and sugar
        if (t['name'] == 'salt' or 'sugar' in t['name']):
            t['quantity'] = t['quantity'] * 2
    
    #if no unhealthy products in recipe, add them
    if counter == 0: 
        ingredient = dict()
        ingredient['name'] = 'butter'
        ingredient['descriptor'] = 'softened'
        ingredient['quantity'] = 1
        ingredient['unit'] = 'stick'
        ingredient['subQuantity'] = -1
        ingredient['subUnit'] = 'N/A'
        recipe['ingredients'].append(ingredient)
        recipe['directions'].append(('Serve with butter.', {}))
    
    # make changes in directions.
    for i in range(0, len(recipe['directions'])):
        recipe['directions'][i] = (re.sub('in oil', 'in pork fat', recipe['directions'][i][0]), recipe['directions'][i][1])
        recipe['directions'][i] = (re.sub('[a-zA-Z]+ oil', 'pork fat', recipe['directions'][i][0]), recipe['directions'][i][1])
        recipe['directions'][i] = (re.sub(', oil', ', pork fat', recipe['directions'][i][0]), recipe['directions'][i][1])


# checks if recipe is dessert. returns true or false
def ifDessert(recipe):
    # check if it is a dessert
    # identify quantity of sugar, chocolate. Make sure it is called before changeUnits is called second time
    q = 0
    for i in recipe['ingredients']:
        if ('sugar' in i['name'] or 'honey' in i['name'] or 'syrup' in i['name'] or 'chocolate' in i['name']):
            q = q + i['quantity']
    if q > 120 or  'pudding mix' in i['name'] or 'cake mix' in i['name']:
        return True
    else:
        return False

# checks if recipe is baked product when main cooking method cannot be changed
def ifBaked(recipe):
    # bakedFood = ['Pie', 'Bread', 'Buns', 'Pizza', 'Cake', 'Scones', 'Tortillas', 'Crackers', 'Pancakes', 'Waffles', 'Shortcakes',
    #			'Focaccia', 'Naan']
    # identify quantity of flour. Make sure it is called before changeUnits is called second time
    q = 0
    for i in recipe['ingredients']:
        temp = re.search('flour', i['name'])
        temp2 = re.search('meal', i['name'])
        if (temp or temp2):
            q = q + i['quantity']
    if q >= 240:
        return True
    else:
        return False


# INDIAN Style
# Indians do not eat pork, beef, bacon, tofu, olive oil, butter, Parmesan
def toIndian(recipe):
    #change recipe name
    for i in intStyle:
        if i in recipe['recipeName']:
            recipe['recipeName'] = re.sub(i, 'Indian ', recipe['recipeName'])
            break
    if 'Indian ' not in recipe['recipeName']:
        recipe['recipeName'] = 'Indian ' + recipe['recipeName']
    #substitute products in title
    recipe['recipeName'] = recipe['recipeName'].lower()
    for i in indianFoodSubsitutes:
        if i in recipe['recipeName']:
            recipe['recipeName'] = re.sub(i, indianFoodSubsitutes[i], recipe['recipeName'])
   # recipe['recipeName'] = re.sub('[a-zA-Z]*(-| )style', '', recipe['recipeName']
    recipe['recipeName'] = recipe['recipeName'].title()

    counter = 0
    # check if not dessert
    if not ifDessert(recipe):
        for t in recipe['ingredients']:
            # change products that are not present in indian cuisine
            for x in indianFoodSubsitutes:
                if x in t['name']:
                    t['name'] = re.sub(x, indianFoodSubsitutes[x], t['name'])
            # change sauce
            temp = re.search('sauce', t['name'])
            if temp or t['name'] == t['name'] == 'ketchup' or t['name'] == 'diced tomatoes' or t[
                'name'] == 'mayonnaise':
                t['name'] = int_sauces.get('indian')
            # change fat
            for x in fats:
                temp = re.search(x, t['name'])
                if temp:
                    t['name'] = int_fats.get('indian')
            # change spices
            # substitute each spice with indian in ingredients and directions
            if 'seasoning' in t['name']:
                t['name'] = int_spices['indian'][counter]
                counter = counter + 1
            if t['name'] in spices:
                #          for i in range(0, len(recipe['directions'])):
                #             recipe['directions'][i] = re.sub(t['name'], int_spices['indian'][counter], recipe['directions'][i])
                t['name'] = int_spices['indian'][counter]
                counter = counter + 1
                if counter > 3:
                    counter = 0

            # change acids
            temp = re.search('vinegar', t['name'])
            temp2 = re.search('wine', t['name'])
            if temp or temp2:
                t['name'] = acids.get('indian')

        # if no spices in recipe but need to add indian flavor
        if counter < 4:
            for x in range(4 - counter):
                ingredient = dict()
                ingredient['name'] = int_spices['indian'][x + counter]
                if checkUnitSystem(recipe) == 'american':
                    ingredient['quantity'] = 1
                    ingredient['unit'] = 'teaspoon'
                else:
                    ingredient['quantity'] = 5
                    ingredient['unit'] = 'ml'
                recipe['ingredients'].append(ingredient)
            recipe['directions'].append(('Season with spices.', {}))


        # make changes in directions.
        for i in range(0, len(recipe['directions'])):
            for key, value in indianFoodSubsitutes.items():
                recipe['directions'][i] = (re.sub(key, value, recipe['directions'][i][0]), recipe['directions'][i][1])

        #substitute spices in directions
            ct = 0
            for j in spices:
                if j in recipe['directions'][i][0]:
                    recipe['directions'][i] = (recipe['directions'][i][0].replace(j, int_spices['indian'][ct]), recipe['directions'][i][1])
                    ct = ct + 1
                    if ct > 3:
                        ct = 0

    else: # ifDessert(recipe):
        counter = 0
        for t in recipe['ingredients']:
            # change products that are not present in indian cuisine
            for x in indianFoodSubsitutes:
                if x in t['name']:
                    t['name'] = re.sub(x, indianFoodSubsitutes[x], t['name'])
            # change spices
            # substitute each spice with indian in ingredients and directions
            if 'seasoning' in t['name']:
                t['name'] = int_dessert_spices['indian'][counter]
                counter = counter + 1
            if t['name'] in spices:
                for i in range(0, len(recipe['directions'])):
                    recipe['directions'][i] = (recipe['directions'][i][0].replace(t['name'], int_dessert_spices['indian'][counter]), recipe['directions'][i][1])

                t['name'] = int_dessert_spices['indian'][counter]
                counter = counter + 1
                if counter > 2:
                    counter = 0
        # if no spices in recipe but need to add indian flavor
        if counter < 3:
            for x in range(3 - counter):
                ingredient = dict()
                ingredient['name'] = int_dessert_spices['indian'][x + counter]
                if checkUnitSystem(recipe) == 'american':
                    ingredient['quantity'] = 1
                    ingredient['unit'] = 'teaspoon'
                else:
                    ingredient['quantity'] = 5
                    ingredient['unit'] = 'ml'
                recipe['ingredients'].append(ingredient)
            recipe['directions'].append(('Season with spices.', {}))


       # make changes in directions.
        for i in range(0, len(recipe['directions'])):
            for key, value in indianFoodSubsitutes.items():
                recipe['directions'][i] = (re.sub(key, value, recipe['directions'][i][0]), recipe['directions'][i][1])
          #substitute spices in directions
            ct = 0
            for j in spices:
                if j in recipe['directions'][i][0]:
                    recipe['directions'][i] = (recipe['directions'][i][0].replace(j, int_dessert_spices['indian'][ct]), recipe['directions'][i][1])
                    ct = ct + 1
                    if ct > 2:
                        ct = 0

# CHINESE Style
def toChinese(recipe):
    #change recipe name
    for i in intStyle:
        if i in recipe['recipeName']:
            recipe['recipeName'] = re.sub(i, 'Chinese ', recipe['recipeName'])
            break
    if 'Chinese ' not in recipe['recipeName']:
        recipe['recipeName'] = 'Chinese ' + recipe['recipeName']

    #substitute products in title
    recipe['recipeName'] = recipe['recipeName'].lower()
    for i in chineseFoodSubsitutes:
        if i in recipe['recipeName']:
            recipe['recipeName'] = re.sub(i, chineseFoodSubsitutes[i], recipe['recipeName'])
   # recipe['recipeName'] = re.sub('[a-zA-Z]*(-| )style', '', recipe['recipeName']
    recipe['recipeName'] = recipe['recipeName'].title()

    counter = 0;
    # check if not dessert
    if not ifDessert(recipe):
        for t in recipe['ingredients']:
            # change products that are not present in chinese cuisine
            for x in chineseFoodSubsitutes:
                if x in t['name']:
                    t['name'] = re.sub(x, chineseFoodSubsitutes[x], t['name'])
            # change sauce
            temp = re.search('sauce', t['name'])
            if temp or t['name'] == 'mayonnaise':
                t['name'] = int_sauces.get('chinese')

            # change fat
            for x in fats:
                temp = re.search(x, t['name'])
                if temp:
                    t['name'] = int_fats.get('chinese')
            # change spices
            # substitute each spice with chinese in ingredients and directions
            if t['name'] in spices:
                if 'seasoning' in t['name']:
                    t['name'] = int_spices['chinese'][counter]
                    counter = counter + 1
                    if counter > 3:
                        counter = 0
                for i in range(0, len(recipe['directions'])):
                    recipe['directions'][i] = (re.sub(t['name'], int_spices['chinese'][counter], recipe['directions'][i][0]), recipe['directions'][i][1])

            # change acids
            temp = re.search('vinegar', t['name'])
            temp2 = re.search('wine', t['name'])
            if temp or temp2:
                t['name'] = acids.get('chinese')
        # if no spices in recipe but need to add chinese flavor
        if counter < 4:
            for x in range(4 - counter):
                ingredient = dict()
                ingredient['name'] = int_spices['chinese'][x + counter]
                if checkUnitSystem(recipe) == 'american':
                    ingredient['quantity'] = 1
                    ingredient['unit'] = 'teaspoon'
                else:
                    ingredient['quantity'] = 5
                    ingredient['unit'] = 'ml'
                recipe['ingredients'].append(ingredient)
            recipe['directions'].append(('Season with spices.',{}))


        # make changes in directions.
        for i in range(0, len(recipe['directions'])):
            for key, value in chineseFoodSubsitutes.items():
                recipe['directions'][i] = (re.sub(key, value, recipe['directions'][i][0]), recipe['directions'][i][1])
            recipe['directions'][i] = (re.sub('[a-zA-Z]+ sauce', int_sauces.get('chinese'), recipe['directions'][i][0]), recipe['directions'][i][1])
            recipe['directions'][i] = (re.sub('ketchup', int_sauces.get('chinese'), recipe['directions'][i][0]), recipe['directions'][i][1])
            recipe['directions'][i] = (re.sub('in oil', 'in ' + int_fats.get('chinese'), recipe['directions'][i][0]), recipe['directions'][i][1])
            recipe['directions'][i] = (re.sub('[a-zA-Z]+ oil', int_fats.get('chinese'), recipe['directions'][i][0]), recipe['directions'][i][1])
            recipe['directions'][i] = (re.sub('[a-zA-Z]+ butter', int_fats.get('chinese'), recipe['directions'][i][0]), recipe['directions'][i][1])
            recipe['directions'][i] = (re.sub('[a-zA-Z]+ wine', acids.get('chinese'), recipe['directions'][i][0]), recipe['directions'][i][1])
            recipe['directions'][i] = (re.sub('[a-zA-Z]+ vinegar', acids.get('chinese'), recipe['directions'][i][0]), recipe['directions'][i][1])

            #substitute spices in directions
            ct = 0
            for j in spices:
                if j in recipe['directions'][i][0]:
                    recipe['directions'][i] = (recipe['directions'][i][0].replace(j, int_spices['chinese'][ct]), recipe['directions'][i][1])
                    ct = ct + 1
                    if ct > 3:
                        ct = 0

    elif ifDessert(recipe) == True:
        counter = 0
        for t in recipe['ingredients']:
            # change products that are not present in chinese cuisine
            for x in chineseFoodSubsitutes:
                if x in t['name']:
                    t['name'] = re.sub(x, chineseFoodSubsitutes[x], t['name'])
            # change spices
            # substitute each spice with chinese in ingredients and directions
            if t['name'] in spices:
                if 'seasoning' in t['name']:
                    t['name'] = int_dessert_spices['chinese'][counter]
                    counter = counter + 1
                    for i in range(0, len(recipe['directions'])):
                        recipe['directions'][i] = re.sub(t['name'], int_dessert_spices['chinese'][counter], recipe['directions'][i])
                        t['name'] = int_dessert_spices['chinese'][counter]
                        counter = counter + 1
                        if counter > 2:
                            counter = 0
        # if no spices in recipe but need to add chinese flavor
        if counter < 3:
            for x in range(3 - counter):
                ingredient = dict()
                ingredient['name'] = int_dessert_spices['chinese'][x + counter]
                if checkUnitSystem(recipe) == 'american':
                    ingredient['quantity'] = 1
                    ingredient['unit'] = 'teaspoon'
                else:
                    ingredient['quantity'] = 5
                    ingredient['unit'] = 'ml'
                recipe['ingredients'].append(ingredient)
            recipe['directions'].append(('Season with spices.', {}))


       # make changes in directions.
        for i in range(0, len(recipe['directions'])):
            for key, value in chineseFoodSubsitutes.items():
                recipe['directions'][i] = (re.sub(key, value, recipe['directions'][i][0]), recipe['directions'][i][1])
          #substitute spices in directions
            ct = 0
            for j in spices:
                if j in recipe['directions'][i][0]:
                    recipe['directions'][i] = (recipe['directions'][i][0].replace(j, int_dessert_spices['chinese'][ct]), recipe['directions'][i][1])
                    ct = ct + 1
                    if ct > 2:
                        ct = 0

# MEXICAN Style
def toMexican(recipe):
        #change recipe name
    for i in intStyle:
        if i in recipe['recipeName']:
            recipe['recipeName'] = re.sub(i, 'Mexican ', recipe['recipeName'])
            break
    if 'Mexican ' not in recipe['recipeName']:
        recipe['recipeName'] = 'Mexican ' + recipe['recipeName']

    #substitute products in title
    recipe['recipeName'] = recipe['recipeName'].lower()
    for i in mexicanFoodSubsitutes:
        if i in recipe['recipeName']:
            recipe['recipeName'] = re.sub(i, mexicanFoodSubsitutes[i], recipe['recipeName'])
   # recipe['recipeName'] = re.sub('[a-zA-Z]*(-| )style', '', recipe['recipeName']
    recipe['recipeName'] = recipe['recipeName'].title()

    counter = 0;
    # check if not dessert
    if not ifDessert(recipe):
        for t in recipe['ingredients']:
            # change products that are not present in mexican cuisine
            for x in mexicanFoodSubsitutes:
                if x in t['name']:
                    t['name'] = re.sub(x, mexicanFoodSubsitutes[x], t['name'])
            # change sauce
            temp = re.search('sauce', t['name'])
            if temp or t['name'] == 'mayonnaise':
                t['name'] = int_sauces.get('mexican')
            # change fat
            for x in fats:
                temp = re.search(x, t['name'])
                if temp:
                    t['name'] = int_fats.get('mexican')
            # change spices
            # substitute each spice with mexican in ingredients and directions
                if t['name'] in spices:
                    if 'seasoning' in t['name']:
                        t['name'] = int_spices['mexican'][counter]
                        counter = counter + 1
                        for i in range(0, len(recipe['directions'])):
                            recipe['directions'][i] = (re.sub(t['name'], int_spices['mexican'][counter], recipe['directions'][i][0]), recipe['directions'][i][1])
                            t['name'] = int_spices['mexican'][counter]
                            counter = counter + 1
                            if counter > 3:
                                counter = 0

            # change acids
            temp = re.search('vinegar', t['name'])
            temp2 = re.search('wine', t['name'])
            if temp or temp2:
                t['name'] = acids.get('mexican')

        # if no spices in recipe but need to add mexican flavor
        if counter < 4:
            for x in range(4 - counter):
                ingredient = dict()
                ingredient['name'] = int_spices['mexican'][x + counter]
                if checkUnitSystem(recipe) == 'american':
                    ingredient['quantity'] = 1
                    ingredient['unit'] = 'teaspoon'
                else:
                    ingredient['quantity'] = 5
                    ingredient['unit'] = 'ml'
                recipe['ingredients'].append(ingredient)
            recipe['directions'].append(('Season with spices.', {}))

        # make changes in directions.
        for i in range(0, len(recipe['directions'])):
            for key, value in mexicanFoodSubsitutes.items():
                recipe['directions'][i] = (re.sub(key, value, recipe['directions'][i][0]), recipe['directions'][i][1])
            recipe['directions'][i] = (re.sub('[a-zA-Z]+ sauce', int_sauces.get('mexican'), recipe['directions'][i][0]), recipe['directions'][i][1])
            recipe['directions'][i] = (re.sub('in oil', 'in ' + int_fats.get('mexican'), recipe['directions'][i][0]), recipe['directions'][i][1])
            recipe['directions'][i] = (re.sub('[a-zA-Z]+ butter', int_fats.get('mexican'),  recipe['directions'][i][0]), recipe['directions'][i][1])
            recipe['directions'][i] = (re.sub('[a-zA-Z]+ wine', acids.get('mexican'), recipe['directions'][i][0]), recipe['directions'][i][1])
            recipe['directions'][i] = (re.sub('[a-zA-Z]+ vinegar', acids.get('mexican'), recipe['directions'][i][0]), recipe['directions'][i][1])

        #substitute spices in directions
            ct = 0
            for j in spices:
                if j in recipe['directions'][i][0]:
                    recipe['directions'][i] = (recipe['directions'][i][0].replace(j, int_spices['mexican'][ct]), recipe['directions'][i][1])
                    ct = ct + 1
                    if ct > 3:
                        ct = 0

    elif (ifDessert(recipe) == True):
        counter = 0
        for t in recipe['ingredients']:
            # change products that are not present in mexican cuisine
            for x in mexicanFoodSubsitutes:
                if x in t['name']:
                    t['name'] = re.sub(x, mexicanFoodSubsitutes[x], t['name'])
            # change spices
            # substitute each spice with mexican in ingredients and directions
            if t['name'] in spices or 'seasoning' in t['name']:
              t['name'] = int_dessert_spices['mexican'][counter]
              counter = counter + 1
              if counter > 2:
                counter = 0
              for i in range(0, len(recipe['directions'])):
                recipe['directions'][i] = (recipe['directions'][i][0].replace(t['name'], int_dessert_spices['mexican'][counter]), recipe['directions'][i][1])

        # if no spices in recipe but need to add mexican flavor
        if counter < 3:
            for x in range(3 - counter):
                ingredient = dict()
                ingredient['name'] = int_dessert_spices['mexican'][x + counter]
                if checkUnitSystem(recipe) == 'american':
                    ingredient['quantity'] = 1
                    ingredient['unit'] = 'teaspoon'
                else:
                    ingredient['quantity'] = 5
                    ingredient['unit'] = 'ml'
                recipe['ingredients'].append(ingredient)
            recipe['directions'].append(('Season with spices.', {}))



       # make changes in directions.
        for i in range(0, len(recipe['directions'])):
            for key, value in mexicanFoodSubsitutes.items():
                recipe['directions'][i] = (re.sub(key, value, recipe['directions'][i][0]), recipe['directions'][i][1])
          #substitute spices in directions
            ct = 0
            for j in spices:
                if j in recipe['directions'][i][0]:
                    recipe['directions'][i] = (recipe['directions'][i][0].replace(j, int_dessert_spices['mexican'][ct]), recipe['directions'][i][1])
                    ct = ct + 1
                    if ct > 2:
                        ct = 0


def toEasy(recipe):
    # make directions more clear for inexperienced cooks
    # explain terms 'minced', 'crushed', 'chopped' if any in ingredients, after directions?
    # fresh juice - regular juice

    #change name
    if 'Easy ' not in recipe['recipeName']:
        recipe['recipeName'] = 'Easy ' + recipe['recipeName']

    cookingTerms = {'saute': 'fry quickly', 'braise': 'fry lightly and then stew slowly with lid on',
                    'poach': 'cook by boiling in a small amount of liquid', 'al dente': 'until just firm',
                    'beat': 'stir rapidly with a whisk', 'blanch': 'cook briefly in boiling water',
                    'bouquet garni': 'parsley, thyme, bay leaves', 'broil': 'cook on a rack under direct heat',
                    'caramelize': 'heat sugar until it becomes a golden syrup', 'chop': 'Cut into bite-sized pieces',
                    'core': 'remove the center',
                    'deep-fry': 'cook immersing in hot fat', 'dice': 'cut into small cubes',
                    'drippings': 'juices from cooking', 'drizzle': 'pour back and forth over food',
                    'glaze': 'coat', 'grease': 'rub with fat',
                    'knead': 'blend together', 'mince': 'cut into tiny peaces',
                    'puree': 'mash', 'sear': 'brown over high heat',
                    'shred': 'cut into narrow strips', 'simmer': 'cook just below the boiling point',
                    'stir-fry': 'quickly cook over high heat', 'whip': 'beat with a whisk or mixer'}

    cheesses = []
    remove_ingredients = []
    #s = list()
    # simlify ingredient list by removing unnesessary details
    for t in recipe['ingredients']:
        if 'freshly ' in t['name']:
            t['name'] = re.sub('freshly ', '', t['name'])
        elif 'vinegar' in t['name']:
            t['name'] = 'vinegar'
        elif 'andouille ' in t['name']:
            t['name'] = re.sub('andouille ', '', t['name'])

        # count nr of cheeses
        if ('cheese' in t['name'] or 'parmesan' in t['name'] or 'mozzarella' in t['name'] or 'Parmesan' in t['name']):
            if t['unit'] != 'N/A':
                cheesses.append(t)
        # delete spices from ingredient list 
        if t['name'] in spices:
        #    s.append(t['name'])
            remove_ingredients.append(t)
    for k in remove_ingredients:
        recipe['ingredients'].remove(k)
    if len(cheesses) > 1:
        # combine several cheeses into one
        for i in range(1, len(cheesses)):
            cheesses[0]['quantity'] = cheesses[0]['quantity'] + cheesses[i]['quantity']
            recipe['ingredients'].remove(cheesses[i])

    for i in range(0, len(recipe['directions'])):
        # substitute cooking terms
        for key, value in cookingTerms.items():
            recipe['directions'][i] = (re.sub(key, value, recipe['directions'][i][0]), recipe['directions'][i][1])
        # remove spices from directions
        for x in spices:
            recipe['directions'][i] = (re.sub(x, '', recipe['directions'][i][0]), recipe['directions'][i][1])
        # substitute cheese
        if len(cheesses) > 1:
            
            recipe['directions'][i] = (re.sub(
                '(\.|,|and)([a-z1-9\/ ,]*)? (mozzarella|ricotta|Parmigiano-Reggiano|Parmesan|cottage|paneer|soy) cheese',
                ' and add cheese', recipe['directions'][i][0]), recipe['directions'][i][1])
   # for item in s:
    #    print(item)


# delete keyowrds in directions seasoning', 'italian seasoning', name of spice as in ingredients with comma, how to soften cream cheese
# CHANGE COOKING METHOD -> finish
# David -> need to parse main cooking method and all others.
def changeMethod(recipe):
    # identify baking recipes that cannot be changed
    # desserts = ['cake', ' buns', ' bread', 'pancakes', 'coctail', 'mousse', 'dessert']
    # for t in dessert:
    #   temp = re.search(t, title)
    #  if temp:
    #     print('Cannot change cooking method for this recipe')
    #    return
    # recipes that cannot be changed. check in title
    l = ['Soup', 'Smoothie', 'Drink', 'Salad', 'Sandwich', 'Coctail']
    if ifDessert(recipe) == True:
        print("We do not recommend to change cooking method for this recipe")
    elif ifBaked(recipe) == True:  # or recipe name in l   <- add
        print("We do not recommend to change cooking method for this recipe")
   # else:
  #    for i in range(0, len(recipe['directions'])):
        #change from baking to stewing
    #    if 'Preheat oven' in recipe['directions'][i][0]:
     #     for i in range(0, len(recipe['directions'])):
      #      recipe['directions'][i] = (re.sub((Place|Arrange) .* baking [a-z]*., 'Arrange', recipe['directions'][i][0]), recipe['directions'][i][1])
       #     recipe['directions'][i] = (re.sub((Place|Arrange) .* baking [a-z]*., 'Arrange', recipe['directions'][i][0]), recipe['directions'][i][1])


def mainCookingMethod(recipe): 

  if 'Baked' in recipe['recipeName']:
    return 'baking'
  elif 'Stir-Fr' in recipe['recipeName']:
    return 'stir-frying'
  elif 'Fried' in recipe['recipeName']:
    return 'frying'
  elif 'Grilled' in recipe['recipeName']:
    return 'grilling'
  elif 'Sandwich' in recipe['recipeName'] or 'Salad' in recipe['recipeName'] or 'Smoothie' in recipe['recipeName']:
    return 'None'
  elif 'Risotto' in recipe['recipeName']:
    return 'simmering'
  elif 'Braised' in recipe['recipeName']:
    return 'braising'


  for i in range(len(recipe['directions'])-1, -1, -1):
#    temp = re.search('preheat( the)? oven', recipe['directions'][i][0])
    temp = re.search('bake(.*)? for [1-9]*', recipe['directions'][i][0])
    temp2 = re.search('bake ', recipe['directions'][i][0])
 #   temp3 = re.search('oven', recipe['directions'][i][0])
    if temp or temp2: #and temp3):
      return 'baking'
    temp3 = re.search('roast ', recipe['directions'][i][0])
    if temp3:
      return 'roasting'
    temp4 = re.search('simmer ', recipe['directions'][i][0])
    if temp4:
      return 'simmering'
    temp4 = re.search('heat the grill ', recipe['directions'][i][0])
    if temp4:
      return 'grilling'
  for i in range(0, len(recipe['directions'])):
    temp4 = re.search('deep(-| )fryer ', recipe['directions'][i][0])
    if temp4:
      return 'deep-frying'
    temp5 = re.search('stir-fry ', recipe['directions'][i][0])
    if temp5:
      return 'stir-frying'
    temp6 = re.search('fry ', recipe['directions'][i][0])
    if temp6:
      return 'frying'
    temp7 = re.search('broiler', recipe['directions'][i][0])
    if temp7:
      return 'broiling'
    temp8 = re.search('frying pan ', recipe['directions'][i][0])
    if temp8:
      return 'frying'
    #if no methods found so far, try again baking
    temp9 = re.search('oven', recipe['directions'][i][0])
    if temp9:
      return 'baking'
    #if no methods found so far, try boiling
    temp9 = re.search('to (a )?boil', recipe['directions'][i][0])
    if temp9:
      return 'boiling'

  #check if slow cooking
  for i in range(0, len(recipe['directions'])):
    temp = re.search('slow cooker', recipe['directions'][i][0])
    if temp:
      return 'slow cooking'
    temp = re.search('saute', recipe['directions'][i][0])
    if temp:
      return 'sauteing'

  #check if boiling
  if 'Soup' in recipe['recipeName']:
    return 'boiling'
  else:
    for i in recipe['ingredients']:
      if 'pasta' in i['name'] or 'spaghetti' in i['name'] or 'macaroni' in i['name']:
        return 'boiling'

  return 'no method found'


def cleanupRecipe(recipe):
    for i in range(0, len(recipe['directions'])):
        str = recipe['directions'][i][0]
        str = re.sub(",[ ]+,", ",", str)
        str = re.sub(" , ", " ", str)
        str = re.sub(" and[ ]*\.", ".", str)
        str = re.sub(",\.", ".", str)
        for u in unitTable:
            if u in recipe['directions'][i][0]:
                str = re.sub("[0-9\/]+ to [0-9\/]+ " + u + "s of ", "", str)
                str = re.sub("about [0-9\/]+ " + u + "s of ", "", str)
                str = re.sub("about [0-9\/]+ " + u + " of ", "", str)
                str = re.sub("[0-9\/]+ " + u + "s of ", "", str)
                str = re.sub("[0-9\/]+ " + u + " of ", "", str)
                str = re.sub("[0-9\/]+ " + u + "s ", "", str)
                str = re.sub("[0-9\/]+ " + u + " ", "", str)
        if str != recipe['directions'][i][0]:
            recipe['directions'][i] = (str, recipe['directions'][i][1])

