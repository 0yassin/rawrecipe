from parser import Ingredient_parser
from requests import request
import requests
# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup
import json

class Ldscraper():
    def __init__(self, url):
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Arch Linux) AppleWebKit/537.36'}
        self.recipe_data = {}

    def fetch(self):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=8)
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script', type='application/ld+json')
            for script in scripts:
                if script.string:
                    try: 
                        data = json.loads(script.string)

                        if isinstance(data, list):
                            for item in data:
                                if self._is_recipe(item): return True        
                        
                        elif isinstance(data, dict):
                            if "@graph" in data:
                                for item in data["@graph"]:
                                    if self._is_recipe(item): return True
                            elif self._is_recipe(data):
                                return True
                    except (json.JSONDecodeError, TypeError):
                                        continue
            return False
        except Exception as e:
            print(f"Error fetching {self.url}: {e}")
            return False



    def _is_recipe(self, item):
        if item.get("@type") == "Recipe":
            self.recipe_data = item
            return True
        return False



    def get_recipe(self):
        parsed_ingredients = []
        parser = Ingredient_parser()

        for ingredient in self.recipe_data.get("recipeIngredient", []):
            parsed_ingredients.append(parser.parse_line(ingredient))
    
        return{
            "title": self.recipe_data.get("name"),
            "author": self.recipe_data.get("author", {}).get("name") if isinstance(self.recipe_data.get("author"), dict) else self.recipe_data.get("author"),

            "ingredients": parsed_ingredients,

            # "ingredients": self.recipe_data.get("recipeIngredient", []),
            "instructions": self._parse_instructions(self.recipe_data.get("recipeInstructions", [])),
            "yields": self.recipe_data.get("recipeYield"),
            "image": self.recipe_data.get("image")
        }

    def _parse_instructions(self, raw_steps):

        parsed_instructions = []
        if not raw_steps:
            return parsed_instructions


        if isinstance(raw_steps, list) and all(isinstance(s, str) for s in raw_steps):
            for idx, step in enumerate(raw_steps):
                parsed_instructions.append({
                    "name": f"Step {idx + 1}",
                    "text": step
                })
            return parsed_instructions


        try:
            target_list = []
            if isinstance(raw_steps, list) and len(raw_steps) > 0:
                if isinstance(raw_steps[0], dict) and 'itemListElement' in raw_steps[0]:
                    target_list = raw_steps[0]['itemListElement']
                else:
                    target_list = raw_steps

            for item in target_list:
                if isinstance(item, dict):
                    parsed_instructions.append({
                        "name": item.get('name', 'Step'),
                        "text": item.get('text', '')
                    })
        except Exception:
            pass
        
        return parsed_instructions

