import re
import scrapeRecipe as scraper
import kitchenCorpus as corpus
from fractions import Fraction
import nltk 


def toNumber(n):
	n = n.lower()
	try:
		return float(n)
	except:
		if '/' in n:
			return float(sum(Fraction(s) for s in n.split()))
		elif 'half' in n or 'halves' in n:
			return float(n.partition(' hal')[0])*0.5
		elif 'quarter' in n:
			return float(n.partition(' quarter')[0])*0.25
		elif 'eighth' in n:
			return float(n.partition(' eighth')[0])*0.125
		else:
			print('error: number not parse-able')
			return 'error: number not parse-able'


def findMeasurementWord(s):
	best = ''
	for word in corpus.measurementWords:
		if word in s:
			if best in word:
				best = word
	return best


def findSubMeasure(s):
	if corpus.subPattern.search(s):
		match = corpus.subPattern.search(s).group(0)
		mWord = ''
		for m in corpus.measurementWords:
			if m in match and len(m)>len(mWord):
				mWord = m
		if len(mWord)>0:
			num = (match.partition('(')[2]).partition(' '+mWord)[0]
			return (num,mWord)
		else:
			return'N/A'
	else:
		return 'N/A'



# typical ingredient format:
# (optional) number -> (optional) measuring size w/ number -> (optional) descriptor i.e. dried -> ingredient -> (optional) state
# should there be a difference between descriptor and state? maybe buy it w/ descriptor, act on it to achieve state
def parseIngredients(unparsedList):
	parsedIngredients = list()

	for i in unparsedList:
		specBayCase = i
		ingredient = i

		subM = 'N/A'
		subMNum = -1
		subMNumRaw = 'N/A'
		quantity = -1
		quantityRaw = 'N/A'
		measurementType = 'N/A'
		descriptor = 'N/A'
		descriptors = list()
		ingredientName = 'N/A'

		tokens = nltk.word_tokenize(i)


		specialCloves = False
		# random special cases
		if 'cloves' in i and not 'garlic' in i:
			specialCloves = True
			i = i.replace('cloves ','')


		# finding sub measurement
		sub = findSubMeasure(i)
		if not sub=='N/A':
			subMNumRaw = sub[0]
			subMNum = toNumber(subMNumRaw)
			subM = sub[1]
			i = i.replace(' ('+subMNumRaw+' '+subM+')','')

		# finding number at beginning
		if corpus.numberPatternBeg.match(i):
			quantityRaw = corpus.numberPatternBeg.match(i).group(0)
			quantity = toNumber(quantityRaw)
			i = i.replace(quantityRaw+' ','')

		# findings main measurement work
		mWord = ''
		for m in corpus.measurementWords:
			if m in i and len(m)>len(mWord):
				mWord = m
		if len(mWord)>0:
			measurementType = mWord
			i = i.replace(mWord+'s','')
			i = i.replace(mWord,'')
		else:
			measurementType = 'N/A'



		ws = nltk.word_tokenize(i)
		for d in corpus.descriptors:
			if d in ws:
				descriptors.append(d)
				i = i.replace(d,'')
				try:
					mod = ws[ws.index(d)-1]
					if(mod in corpus.descriptorMods):
						i = i.replace(mod,'')
				except:
					i=i


		# this first partition may be a bad idea
		ingredientName = i.partition(',')[0]
		ingredientName = re.sub(r'\([^)]*\)', '', ingredientName)
		ingredientName = ingredientName.partition(' to ')[0]
		ingredientName = ingredientName.replace(',','').replace(';','').replace('\'','').replace('.','').replace('(','').replace(')','').replace('\"','')
		ingredientName = ingredientName.strip()


		if specialCloves:
			ingredientName = ingredientName+'cloves'



		if (('leaves' in specBayCase) or ('leaf' in specBayCase)) and ('bay' in specBayCase):
			if corpus.numberPatternBeg.match(specBayCase):
				quantityRaw = corpus.numberPatternBeg.match(specBayCase).group(0)
				quantity = toNumber(quantityRaw)
				if quantity == 1:
					ingredientName = 'bay leaf'
					measurementType  = 'N/A'
				else:
					ingredientName = 'bay leaves'
					measurementType  = 'N/A'


		ingredient = dict()
		# Compiling parsed information into dictionary
		ingredient['subUnit'] = subM
		ingredient['subQuantity'] = subMNum
		ingredient['unit'] = measurementType
		ingredient['quantity'] = quantity
		ingredient['name'] = ingredientName
		ingredient['descriptors'] = descriptors

		# print(ingredient)
		parsedIngredients.append(ingredient)


	return parsedIngredients

	# with open('obj/ingredientSet.pkl', 'rb') as f:
	# 	ingredientSet = pickle.load(f)

	# for i in parsedIngredients:
	# 	ingredientSet.add(i['name'])

	# with open('obj/ingredientSet.pkl', 'wb') as f:
	# 	pickle.dump(ingredientSet, f, pickle.HIGHEST_PROTOCOL)




def findTime(s):
	hours = 0
	minutes = 0
	s = s.lower()
	if corpus.timePattern.search(s):
		try:
			match = corpus.timePattern.search(s).group(0)
			if 'hour' in match:
				hours = int(match.partition(' hour')[0])
				if 'hours' in match:
					match = ((match.partition('hours')[2]).replace('and','')).strip()
				else:
					match = ((match.partition('hour')[2]).replace('and','')).strip()
			if 'minute' in match:
				minutes = int(match.partition(' minute')[0])
			t = (hours,minutes)	
			return t
		except:
			return 'N/A'
	else:
		return 'N/A'

def findTemperature(s):
	num = -1
	unit = 'N/A'
	s = s.lower()
	if corpus.temperaturePattern.search(s):
		try:
			match = corpus.temperaturePattern.search(s)
			tempUnit = 'N/A'
			if 'degrees' in s:
				num = float(nltk.word_tokenize(s.partition(' degrees')[0])[-1])
				tempUnit = nltk.word_tokenize(s.partition('degrees ')[2])[0]
			if '\u00b0' in s:
				num = float(nltk.word_tokenize(s.partition('\u00b0')[0])[-1])
				tempUnit = nltk.word_tokenize(s.partition('\u00b0')[2])[0]
			if tempUnit == 'c' or tempUnit == 'celcius':
				unit = 'celcius'
			elif tempUnit == 'f' or tempUnit == 'fahrenheit':
				unit = 'fahrenheit'
			return (num,unit)
		except:
			return 'N/A'
	else:
		return 'N/A'

# break them up into smaller steps
# find all kitchen appliances and utensils 
# find cooking time or cooking conditional for each step
# each cooking step should have:
# ingredient(s)
# utensil(s)
# appliance(s)
# cooking time and/or stop condition
# initial ingredient state
# final ingredient state



# create way to find ingredient in direction if not perfectly listed
# e.g. beef instead of beef short rib
def parseDirections(unparsedList,ingredientsList):
	
	# preparing information to use
	allIngredients = list()
	for ingredient in ingredientsList:
		if not ingredient['name']=='N/A':
			allIngredients.append(ingredient['name'])

	ingredientWordBag = list()
	for i in allIngredients:
		words = nltk.word_tokenize(i)
		for w in words:
			ingredientWordBag.append(w)

	unparsedSteps = list()
	for i in unparsedList:
		sentences = nltk.sent_tokenize(i)
		for s in sentences:
			unparsedSteps.append(s.lower())

	unparsedSteps2 = list()
	# starting actual parse
	parsedSteps = list()
	# decide on parsing routine
	# note: steps with ; are really two steps just involving the same ingredients
	# u and u2 thing might not work... maybe remove later
	for u in unparsedSteps:
		twoStep = False
		u2=''
		temp = u.split(';')
		if len(temp) == 2:
			twoStep = True
			u2 = temp[1]
			u = temp[0]

		ingredients = list() # contains (nameInDirection,nameInIngredientList) tuples
		prepAction = 'N/A'
		cookAction = 'N/A'
		tools = list() # maybe find way to split tools by use later... cook, prep, appliance, cookware, utensil
		stepTime = 'N/A' # (int,int)  showing (hours,minutes)
		temperature = 'N/A' # will be tuple with (temperature (int),unit)

		# finding ingredients involved in this step
		for i in allIngredients:
			if (i in u) and (not nltk.word_tokenize(u)[0]==i):
				ingredients.append((i,i))
			else:
				ws = nltk.word_tokenize(i)
				for w in ws:
					if (w in u) and (not nltk.word_tokenize(u)[0]==w) and (not w in corpus.junkWords): #if (w in u) and (ingredientWordBag.count(w) == 1):
						ingredients.append((w,i))
						break


		# finding prep actions
		for p in corpus.prepActions:
			if p in u:
				prepAction = p
				break

		for c in corpus.cookActions:
			if c in u:
				cookAction = c
				break


		# maybe include certain tools based off of cook/prep actions, i.e. if see bake, add oven
		uWords = nltk.word_tokenize(u)
		for w in uWords:
			if (w in corpus.cookware) or (w in corpus.utensils) or (w in corpus.cookAppliances) or (w in corpus.prepAppliances):
				tools.append(w)
			if ('bake' in u) and (not 'oven' in tools):
				tools.append('oven')

		# find time patterns
		stepTime = findTime(u)

		# find temperature patterns
		temperature = findTemperature(u)


		step = dict()
		step['ingredients'] = ingredients
		step['prepAction'] = prepAction
		step['cookAction'] = cookAction
		step['tools'] = tools
		step['time'] = stepTime
		step['temperature'] = temperature


		prepAction2 = 'N/A'
		cookAction2 = 'N/A'
		tools2 = list()
		stepTime2 = 'N/A'
		temperature2 = 'N/A'
		if twoStep:

			for p in corpus.prepActions:
				if p in u2:
					prepAction2 = p
					break

			for c in corpus.cookActions:
				if c in u2:
					cookAction2 = c
					break

			u2Words = nltk.word_tokenize(u2)
			for w in u2Words:
				if (w in corpus.cookware) or (w in corpus.utensils) or (w in corpus.cookAppliances) or (w in corpus.prepAppliances):
					tools2.append(w)
				if ('bake' in u2) and (not 'oven' in tools2):
					tools.append('oven')

			stepTime2 = findTime(u2)
			temperature2 = findTemperature(u2)

		step2 = dict()
		step2['ingredients'] = ingredients
		step2['prepAction'] = prepAction2
		step2['cookAction'] = cookAction2
		step2['tools'] = tools2
		step2['time'] = stepTime2
		step2['temperature'] = temperature2		


		if twoStep:
			# adding another unparsed occurence to allow proper zip
			#unparsedSteps.insert(unparsedSteps.index(u)+1,u)
			unparsedSteps2.append(u) # definitely a better way to this, like just above...
			unparsedSteps2.append(u2)
			parsedSteps.append(step)
			parsedSteps.append(step2)
		else:
			parsedSteps.append(step)
			unparsedSteps2.append(u)


	return list(zip(unparsedSteps2,parsedSteps))




def parseRecipe(recipe):
	ingredients = recipe['ingredients']
	directions = recipe['directions']

	parsedIngredients = parseIngredients(ingredients)
	# for i in parsedIngredients:
	# 	print(i)
	parsedDirections = parseDirections(directions,parsedIngredients)

	return (parsedIngredients,parsedDirections)


# url = input('Please enter a recipe url from AllRecipes.com: ')
# recipe = scraper.scrapeRecipe(url)

# z = parseRecipe(recipe)

# for y in z:
# 	print(y)

# temp = '4 523 1/2 5.4 6/5'
# p = '(\d+\.\d+$)|((\d+ )?\d+\/\d+$)|(\d+ (([hH]alf)|([hH]alves)|([qQ]uarter)|([eE]ighth))$)|(\d+$)'
# pat = re.compile(p)
# t = pat.search(temp).group(0)
# print(t)


