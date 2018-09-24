# -*- coding: utf-8 -*-
import copy

from Proj2 import *

# load recipe
url = input('Please enter a recipe url from AllRecipes.com: ')
recipe = scraper.scrapeRecipe(url)

# parse recipe
recipe['ingredients'] = parser.parseIngredients(recipe['ingredients'])
recipe['directions'] = parser.parseDirections(recipe['directions'], recipe['ingredients'])

# cleanup directions
directions = []
repeats = []
for d in recipe['directions']:
    if d[0] in directions:
        repeats.append(d)
    else:
        directions.append(d[0])
for r in repeats:
    recipe['directions'].remove(r)

for t in recipe['ingredients']:
    if 'skinless' in t['name']:
        t['name'] = 'chicken breasts'

orig_recipe = copy.deepcopy(recipe)

# print options
exit = False
while not exit:

    printRecipe(recipe)
    print('')
    print("Main cooking method: " + mainCookingMethod(recipe))
    print('')
    print('-------------------------------------')
    print('Choose option: ')
    print('   0 : transform to Vegan')
    print('   1 : transform to Vegetarian')
    print('   2 : transform to Non-Vegetarian')
    print('   3 : transform to Mexican')
    print('   4 : transform to Chinese')
    print('   5 : transform to Indian')
    print('   6 : transform to Indian Vegetarian')
    print('   7 : transform to Indian Vegan')
    print('   8 : transform to Healthy')
    print('   9 : transform to Unhealthy')
    print('   e : transform to Easy')
    print('   u : change units (metric/american)')
    print('   z : back to original recipe')
 #   print('   i : internal representation')
    print('   x : exit')
    key = input(':')

    if key == 'x':
        break

    if key == 'u':
        changeUnits(recipe)
        cleanupRecipe(recipe)
    if key == '0':
        recipe = copy.deepcopy(orig_recipe)
        changeUnits(recipe)
        toVegan(recipe)
        changeUnits(recipe)
    if key == '1':
        recipe = copy.deepcopy(orig_recipe)
        changeUnits(recipe)
        toVegetarian(recipe)
        changeUnits(recipe)
    if key == '2':
        recipe = copy.deepcopy(orig_recipe)
        changeUnits(recipe)
        toNonVegetarian(recipe)
        changeUnits(recipe)
    if key == '3':
        recipe = copy.deepcopy(orig_recipe)
        changeUnits(recipe)
        toMexican(recipe)
        changeUnits(recipe)
    if key == '4':
        recipe = copy.deepcopy(orig_recipe)
        changeUnits(recipe)
        toChinese(recipe)
        changeUnits(recipe)
    if key == '5':
        recipe = copy.deepcopy(orig_recipe)
        changeUnits(recipe)
        toIndian(recipe)
        changeUnits(recipe)
    if key == '6':
        recipe = copy.deepcopy(orig_recipe)
        changeUnits(recipe)
        toVegetarian(recipe)
        toIndian(recipe)
        changeUnits(recipe)
    if key == '7':
        recipe = copy.deepcopy(orig_recipe)
        changeUnits(recipe)
        toVegan(recipe)
        toIndian(recipe)
        changeUnits(recipe)
    if key == '8':
        recipe = copy.deepcopy(orig_recipe)
        changeUnits(recipe)
        toHealthy(recipe)
        cleanupRecipe(recipe)
        changeUnits(recipe)
    if key == '9':
        recipe = copy.deepcopy(orig_recipe)
        changeUnits(recipe)
        toUnhealthy(recipe)
        cleanupRecipe(recipe)
        changeUnits(recipe)
    if key == 'e':
        units = checkUnitSystem(recipe)
        if units == 'american':
            changeUnits(recipe)
        toEasy(recipe)
        if units == 'american':
            changeUnits(recipe)
        cleanupRecipe(recipe)
    if key == 'z':
        recipe = copy.deepcopy(orig_recipe)
   # if key == 'i':
    #    for t in recipe['ingredients']:
     #       print (t['name'])
      ##      print (t['descriptor'])
       #     print (t['descriptors'])
        #    print (t['quantity'])
        #    print (t['unit'])
        continue
