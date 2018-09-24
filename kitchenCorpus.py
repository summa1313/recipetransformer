
import re



def patternBuilder(ls):
	pat = '('
	for s in ls:
		pat = pat+s+'|'
	pat = pat[:-1]+')'
	return pat


def bestMatch(s,patternSet):
	return


# fine for now but could be improved to include more formats
numPatternRaw = '(\d+\.\d+)|((?:\d+ )?\d+\/\d+)|(\d+ (?:(?:[hH]alf)|(?:[hH]alves)|(?:[qQ]uarter)|(?:[eE]ighth)))|(\d+)'
numberPattern = re.compile(numPatternRaw)
endStringNum = '(\d+\.\d+$)|((?:\d+ )?\d+\/\d+$)|(\d+ (?:(?:[hH]alf)|(?:[hH]alves)|(?:[qQ]uarter)|(?:[eE]ighth))$)|(\d+$)'
numberPatternEnd = re.compile(endStringNum)
begStringNum = '(^\d+\.\d+)|(^(?:\d+ )?\d+\/\d+)|(^\d+ (?:(?:[hH]alf)|(?:[hH]alves)|(?:[qQ]uarter)|(?:[eE]ighth)))|(^\d+)'
numberPatternBeg = re.compile(begStringNum)


# keep adding more, remove space after can?????
measurementWords = ['cup','ounce','oz','quart','gallon','pint','tablespoon','teaspoon','pound','lb','tbs',
'tps','pinch','scoop','handful','can','gram','drop','liter','dollop','bag','milligram','kilogram','mg','kg','ml'
'milliliter','fl oz','fluid ounce','carton','dozen','inch','inches','centimeter','centimeters','fillet','handful'
'jar','package','container','bottle','slice','leaves','leaf','loaf','loaves','bunch','bunches'
'scoop','carton','packet','tub','bar','bulb','clove','piece','tub','ear','stalk','head']

unitPatternRaw = patternBuilder(measurementWords)

subPattern = re.compile('\((?:'+numPatternRaw+') '+unitPatternRaw+'\)')

unitPattern = re.compile('('+unitPatternRaw+') ')

descriptors = ['minced','chopped','sliced','smashed','seeded','shredded','dried','cubed','deveined', 'ground', 'canned', 'peeled',
'large','medium','small','frozen','grated','fresh','picked','cold','crushed','cooked','lean','bulk','divided','optional','whole',
'pitted','quartered','melted','unsalted','halved','juiced','divided','mild','spicy','chunky','rinsed']

descriptorMods = ['finely','freshly','coarsely','and','with']

prepAppliances = ['blender','food processor','mixer','mandoline','spiralizer']
# words to review: grill
cookAppliances = ['oven','stove','broiler','gas grill','charcoal grill','grill','toaster','rice cooker',
'pressure cooker','fryer']

utensils = ['knife','blade','whisk','spoon','spatula','tongs','bowl','baking dish','dish','grater']

#sheet, colander (is it cookware?)
cookware = ['pot','pan','baking sheet','sheet','skillet','colander','saucepan','aluminum foil','baking paper','wax paper',
'baking tin','dutch over']

cookwareModifiers = ['cast-iron','cast iron','non stick','non-stick']


# questionable words: flip, whisk, stir in
prepActions = ['stir in','stir','mix in','mix','chop','slice','flip','whisk','devein','julienne','score','combine',
'pour','skin','skim','dissolve','shape','drain','discard','blend','sprinkle','uncover','cover']


cookActions = ['bake','sear','stir fry','sautee','saut\u00E9e','broil','fry','flamb\u00E9',
'scortch','reduce','boil','simmer','preheat','heat']

# maybe look for until ... phrases
cookConditions = ['tender','until thickened','bubbling','lightly browned','browned']


prepositions = ['while','when','during','before','after']


junkWords = ['and','with','of','or']


timePattern = re.compile('(\d+ hour(?:s?) (?:and )?\d+ minute(?:s?))|(\d+ minute(?:s?))|(\d+ hour(?:s?))')


temperaturePattern = re.compile('(\d+(?:(?: [dD]egrees)|(?:\u00b0)) (?:(?:[fF]ahrenheit)|(?:[fF])|(?:[Cc]elcius)|(?:[cC])))')




