from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


def cleanTime(time):
	time = time.strip()
	hours = 0
	minutes = 0
	if 'h' in time:
		hours = int(time.partition(' h')[0])
		time = time.partition('h ')[2]
	if 'm' in time:
		minutes = int(time.partition(' m')[0])
	return (hours,minutes)

# all numbers in float form, try int or int/float mix?
def scrapeRecipe(url):
	file = urlopen(url)
	html = file.read()
	bsoup = BeautifulSoup(html,'html.parser')


	recipeName = bsoup.find('h1', {'class': re.compile('recipe-summary__h1')}).text

	# serving size
	servingsMeta = bsoup.find('meta', {'id':'metaRecipeServings'})
	servings = float(servingsMeta.attrs['content'])

	# ingredients
	ingredientsList1 = bsoup.find('ul', {'id': re.compile('lst_ingredients_1')}).findAll('label')
	ingredientsList2 = bsoup.find('ul', {'id': re.compile('lst_ingredients_2')}).findAll('label')
	ingredients = list()
	for i in ingredientsList1:
		try:	
			ingredients.append(i.attrs['title'])
		except:
			break
	for i in ingredientsList2:
		try:
			ingredients.append(i.attrs['title'])
		except:
			break

	# directions
	directionsSection = bsoup.find('div',{'class': re.compile('directions--section__steps')})
	try:
		prepTime = directionsSection.find('time', {'itemprop': re.compile('prepTime')}).text
		cookTime = directionsSection.find('time', {'itemprop': re.compile('cookTime')}).text
		totalTime = directionsSection.find('time', {'itemprop': re.compile('totalTime')}).text
	except:
		prepTime = 'N/A'
		cookTime = 'N/A'
		totalTime = 'N/A'
	directionsSpans = directionsSection.findAll('span', {'class': re.compile('recipe-directions__list--item')})
	directions = list()
	for d in directionsSpans:
		t = d.text
		if len(t)>0:
			directions.append(t)

	# nutrition
	try:
		nutritionSection = bsoup.find('section', {'itemprop': re.compile('nutrition')})
		calories = nutritionSection.find('span',{'itemprop': re.compile('calories')}).text
		fatContent = float(nutritionSection.find('span',{'itemprop': re.compile('fatContent')}).text)
		carbohydrateContent = float(nutritionSection.find('span',{'itemprop': re.compile('carbohydrateContent')}).text)
		proteinContent = float(nutritionSection.find('span',{'itemprop': re.compile('proteinContent')}).text)
		cholesterolContent  = float(nutritionSection.find('span',{'itemprop': re.compile('cholesterolContent')}).text)
		sodiumContent = float(nutritionSection.find('span',{'itemprop': re.compile('sodiumContent')}).text)
	except:
		calories = -1
		fatContent = -1
		carbohydrateContent = -1
		proteinContent = -1
		cholesterolContent  = -1
		sodiumContent = -1


	# cleaning data
#    try:
#        prepTime = cleanTime(prepTime)
#        cookTime = cleanTime(cookTime)
#        totalTime = cleanTime(totalTime)
#    except:
#        prepTime = -1
#        cookTime = -1
#        totalTime = -1
	if not calories == -1:
		calories = float(calories.partition(' calories')[0])
	nutritionFacts = dict()
	nutritionFacts['calories'] = calories
	nutritionFacts['fat'] = fatContent
	nutritionFacts['carbs'] = carbohydrateContent
	nutritionFacts['protein'] = proteinContent
	nutritionFacts['cholesterol'] = cholesterolContent
	nutritionFacts['sodium'] = sodiumContent


	# putting scraped info into useful data format for later use
	recipeInfo = dict()
	recipeInfo['recipeName'] = recipeName
	recipeInfo['servings'] = servings
#    recipeInfo['prepTime'] = prepTime
#    recipeInfo['cookTime'] = cookTime
#    recipeInfo['totalTime'] = totalTime
	recipeInfo['ingredients'] = ingredients
	recipeInfo['directions'] = directions
	recipeInfo['nutrition'] = nutritionFacts

	return recipeInfo
