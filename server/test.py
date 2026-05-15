from scraper import Ldscraper
from parser import Ingredient_parser 

parser = Ingredient_parser()
scraper = Ldscraper("https://iambaker.net/coffee-sugar-cookies/")

if scraper.fetch():
    recipe = scraper.get_recipe()

    parsed_ingredients = []
    for ingredient in recipe["ingredients"]:
        parsed_ingredients.append(parser.parse_line(ingredient))
    
    for parsed_ingredient in parsed_ingredients:
        print(parsed_ingredient)