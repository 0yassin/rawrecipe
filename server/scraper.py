from requests import request
import requests
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
        return{
            "title": self.recipe_data.get("name"),
            "author": self.recipe_data.get("author", {}).get("name") if isinstance(self.recipe_data.get("author"), dict) else self.recipe_data.get("author"),
            "ingredients": self.recipe_data.get("recipeIngredient", []),
            "instructions": self._parse_instructions(self.recipe_data.get("recipeInstructions", [])),
            "yields": self.recipe_data.get("recipeYield"),
            "image": self.recipe_data.get("image")
        }

    def _parse_instructions(self, raw_steps):

        parsed_instructions = []

        if raw_steps[0]['itemListElement']:
            for item in raw_steps[0]['itemListElement']:
                # parsed_instructions.append(item['text'])
                parsed_instructions.append({
                    "name": item['name'],
                    "text": item['text'],
                })

        # return raw_steps[0]['itemListElement'
        return parsed_instructions

