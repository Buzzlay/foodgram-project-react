import json

with open('ingredients.json') as ing:
    raw_ingredients = json.load(ing)

ingredients = list()
for raw in raw_ingredients:
    ingredients.append({
        'model': 'recipes.ingredient',
        'fields': raw,
    })

with open('ingredients.json', 'w') as dest:
    json.dump(ingredients, dest)
