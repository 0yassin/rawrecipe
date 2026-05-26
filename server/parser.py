from bs4 import ResultSet
import unicodedata
import unicodedata
import re
from fractions import Fraction

class Ingredient_parser:
    def __init__(self):
        self.number_pattern = r'(?P<quantity>\d+\s+(?:and\s+)?\d/\d|\d+\s+\d+\.\d+|\d+\s+\d/\d|\d/\d|\d+\.\d+|\d+)'
        self.units = {
            "cup": ["cup", "cups", "c."],
            "tablespoon": ["tablespoon", "tablespoons", "tbsp", "tbs", "tbsp."],
            "teaspoon": ["teaspoon", "tsp", "teaspoons", "tsp."],
            "gram": ["gram", "grams", "g", "g."],
            "kilogram": ["kilogram", "kg", "kg.", "kilograms"],
            "milliliter": ["milliliter", "milliliters", "ml", "ml."],
            "pound": ["pounds", "lb", "pound", "lbs"]
        }

    def parse_quantity(self, quantity_str):
            try: 
                clean_str = quantity_str.replace('and', ' ').strip()

                parts = clean_str.split()
                
                total = 0

                for part in parts:
                    total += float(Fraction(part))
                return total
            except (ValueError, ZeroDivisionError): return 0.0





    def parse_line(self, raw_string):
            raw_string = raw_string.replace('&amp;', '&').replace('\xa0', ' ')
            raw_string = self.parse_unicode_fraction(raw_string)
            match = re.search(self.number_pattern, raw_string)


            # quantity_raw = match.group('quantity') if match else "0"
            # quantity = self.parse_quantity(quantity_raw)

            if match: 
                quantity_raw = match.group('quantity')
                quantity = self.parse_quantity(quantity_raw)
                remaining_text = raw_string.replace(quantity_raw, "", 1).strip()

            else:
                quantity = 1.0
                remaining_text = raw_string.strip()

            # remaining_text = raw_string.replace(quantity_raw, "").strip()

            remaining_text = re.sub(r'\(.*?\)', '', remaining_text).strip()

            found_unit = None


            for unit_key, alieases in self.units.items():
                for alias in alieases:
                    if re.search(rf'\b{re.escape(alias)}\b', remaining_text,flags=re.I):
                        found_unit = unit_key
                        remaining_text = re.sub(rf'\b{re.escape(alias)}\b', '', remaining_text, re.I)
                        break
                if found_unit: break

            name = re.sub(r'^of\s+', '', remaining_text).strip()

            return {
                "text": raw_string,
                "quantity": quantity,
                "unit":found_unit,
                "name":name,
            }

        
    def parse_unicode_fraction(self, text):
        result = []
        for char in text:
            try:
                if "FRACTION" in  unicodedata.name(char):
                    value = unicodedata.numeric(char)
                    result.append(f" {value} ")
                else:
                    result.append(char)
            except (ValueError, KeyError):
                result.append(char)
        return "".join(result)



    # def parse_instructions(self, instructions):
