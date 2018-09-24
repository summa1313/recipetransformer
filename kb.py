#KNOWLEDGE BASE -> maybe create separate file for it

spices = ['allspice', 'anise', 'annatto seed', 'barberry', 'basil', 'bay leaf', 'Cajun seasoning', 'caper',
          'caraway seed', 'cardamom', 'cinnamon',
          'cayenne pepper', 'celery salt', 'celery seed', 'chili pepper', 'chives', 'cilantro', 'cinnamon', 'clove',
          'coriander', 'cumin', 'curry', 'dill', 'fennel', 'horseradish', 'jalapeno', 'jasmine flowers',
          'juniper berries', 'garlic powder', 'cajun seasoning',
          'lime leaves', 'lavender', 'lemongrass', 'marjoram', 'mint', 'mustard', 'nutmeg', 'oregano', 'paprika',
          'pepper black', 'peppermint', 'poppy seed', 'rosemary', 'saffron', 'serrano',
          'sesame seed', 'sorrel', 'spearmint', 'anise', 'sumac', 'szechuan pepper', 'tarragon', 'thyme', 'turmeric',
          'vanilla', 'vanilla extract', 'wasabi', 'Italian seasoning', 'almond extract', 'orange peel',
          'candied ginger', 'italian seasoning', 'chipotle', 'Mexican oregano',
          'Mexican vanilla', 'Mexican cinnamon', 'orange zest', 'lemon pepper', 'bay leaf', 'bay leaves']

# to do: check brisket beef
vegetarian_substitutes = {'pot roast': 'Gardein Vegetarian Beef', 'chicken thighs': 'eggplant',
                          'beef bouillon': 'vegetable bouillon', 'chicken broth': 'vegetable broth', 'beef broth': 'water',
                          'chicken stock': 'water', 'beef stock': 'water', 'steak': 'eggplant', 'fish stock': 'water',
                          'beef': 'canned lentils', 'brisket': 'portobello', 'pork chops': 'vegan meat',
                          'lamb': 'soya chunks', 'chicken': 'eggplant', 'turkey': 'seitan', 'duck': 'portobello mushrooms',
                          'anchovy fillet': 'seaweed', 'anchovies': 'seaweed', 'ham': 'vegan ham', 'cooked ham': 'vegan ham',
                          'bacon': 'veggie bacon', 'sausage': 'vegetarian sausage', 'lard': 'margarine',
                          'fish': 'tofu', 'salmon': 'carrots', 'tuna': 'fishless tuna', 'scallops': 'tofu',
                          'crab': 'hearts of palm', 'schrimps': 'hearts of palm', 'prosciutto': 'veggie bacon',
                          'game hen': 'eggplant', 'halibut': 'eggplant', 'shrimp': 'vegan prawn', 'ribs': 'canned lentils', 'baby back': '',
                          'meatballs': 'vegan meatballs', 'pork fat': 'vegetable oil' }

vegan_substitutes = {'egg': 'vegan egg', 'milk': 'almond milk', 'buttermilk': 'soy yogurt', 'sour cream': 'soy yogurt',
                     'cream': 'full fat coconut milk', 'butter': 'margarine', 'mayonnaise': 'hummus',
                     'yogurt': 'soy yogurt', 'cottage cheese': 'vegan cheese', 'gruyere cheese': 'soy cheese',
                     'Parmesan': 'soy cheese', 'Parmigiano-Reggiano cheese': 'soy cheese',
                     'Parmigiano-Reggiano': 'soy cheese', 'mozzarella': 'vegan cheese',
                     'cheese': 'soy cheese', 'creme fraiche': 'soy yogurt', 'camembert cheese': 'vegan cheese'}

fats = ['[a-z]* oil', '[a-z]* fat', 'ghee', 'margarine', 'shortening']

int_spices = {'indian': ['turmeric', 'cumin', 'cloves', 'ground cardamom'],
              'mexican': ['chipotle', 'coriander', 'mexican oregano', 'majoram'],
              'chinese': ['ginger', 'anise', 'red chili prepper', 'fennel seeds']}
int_dessert_spices = {'indian': ['Indian cinnamon', 'cardamom', 'nutmeg', 'cinnamon', 'cardamom'],
                      'mexican': ['Mexican vanilla', 'Mexican cinnamon', 'orange zest', 'Mexican vanilla',
                                  'Mexican cinnamon'],
                      'chinese': ['candied ginger', 'almond extract', 'orange peel', 'almond extract', 'orange peel']}

int_fats = {'indian': 'ghee', 'chinese': 'sesame oil', 'mexican': 'canola oil'}
int_sauces = {'indian': 'сurry sauce', 'chinese': 'sweet and sour sauce', 'mexican': 'salsa'}
acids = {'indian': 'lemon juice', 'chinese': 'rice vinegar', 'mexican': 'lime juice'}

indianFoodSubsitutes = {'beef bouillon': vegetarian_substitutes['beef bouillon'], 'beef': 'lamb',
                        'steaks': 'lamb chops', 'Italian sausage': 'chicken sausage', 'pork chops': 'lamb chops',
                        'buttermilk': 'yogurt', 'butter': int_fats.get('indian'), 'pork': 'lamb', 'parmesan': 'Kalimpong',
                        'bacon': vegetarian_substitutes['bacon'], 'Camembert cheese': 'soft Indian cheese',
                        'tofu': 'red bean paste', 'ricotta': 'paneer', 'mozzarella': 'paneer', 'Italian-style': 'Indian-style',
                        'Parmesan cheese': 'Kalimpong cheese', 'camembert cheese': 'soft Indian cheese',
                        'Parmigiano-Reggiano': 'Kalimpong cheese', 'jalapeno': 'chili', 'Parmesan': 'Kalimpong cheese',
                        'Worcestershire sauce': 'chile sauсe', 'Cheddar cheese': 'paneer', 'Mexican-style': 'Indian-style',
                        '[a-zA-Z]+ sauce':int_sauces.get('indian'), 'Romano cheese': 'soft Indian cheese',
                        'ketchup': int_sauces.get('indian'), 'parmesan cheese': 'Kalimpong cheese', 'steak': 'lamb steak',
                        'mayonnaise': int_sauces.get('indian'), 'Gruyere cheese': 'paneer', 'romano cheese': 'soft Indian cheese',
                        'diced tomatoes': int_sauces.get('indian'), 'gruyere cheese': 'paneer', 'poblano peppers': 'sweet peppers',
                        'in oil': 'in ' + int_fats.get('indian'), 'Parmesan': 'Kalimpong Cheese', 'lard': 'margarine',
                        '[a-zA-Z]+ oil': int_fats.get('indian'), '[a-zA-Z]+ butter': int_fats.get('indian'),
                        '[a-zA-Z]+ wine': acids.get('indian'), '[a-zA-Z]+ vinegar': acids.get('indian')}
chineseFoodSubsitutes = {'butter': int_fats.get('chinese'), 'ricotta': 'soft cheese', 'mozzarella': 'soft cheese', 'poblano peppers': 'sweet peppers',
                         'Parmesan cheese': 'hard cheese', 'parmesan cheese': 'hard cheese', 'Romano cheese': 'soft cheese', 'Mexican-style': 'Indian-style',
                         'Parmesan': 'hard cheese', 'Parmigiano-Reggiano': 'hard cheese', 'jalapeno': 'chili', 'camembert cheese':'soft cheese',
                         'Worcestershire sauce': 'chile sauce', 'Camembert cheese': 'soft cheese', 'Italian-style': 'Chinese-style'}
mexicanFoodSubsitutes = {'tofu': 'red bean paste', 'ricotta': 'Queso Fresco', 'Gruyere cheese': 'Mexican cheese',
                         'mozzarella': 'Queso Fresco', 'romano cheese': 'Queso Manchego','Parmesan cheese': 'Queso Manchego', 'Romano cheese': 'soft Mexican cheese',
                         'Parmesan': 'Queso Manchego', 'Camembert cheese': 'Queso Manchego', 'gruyere cheese': 'Mexican cheese',
                         'Parmigiano-Reggiano': 'Queso Manchego', 'Italian-style': 'Mexican-style', 'camembert cheese':'Queso Manchego', 'Worcestershire sauce': 'Tabasco sauce', 'parmesan': 'Queso Manchego'}

# American To Metric Conversion Table, volume to ml, weight to g and kg
unitTable = {'gallon': 3785, 'quart': 950, 'pint': 475, 'cup': 240, 'oz': 30, 'tablespoon': 15, 'teaspoon': 5}
unconvertibleUnits = ['container', 'clove', 'pinch', 'package', 'can', 'stalk', 'stick', 'bunch', 'bottle', 'piece', 'slice', 'inch', 'leaf' 'leaves']

intStyle = {'Indian ', 'Italian ', 'Chinese ', 'Mexican '}
