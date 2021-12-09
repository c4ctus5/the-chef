#!/usr/bin/pyton3

import json
import requests
from bs4 import BeautifulSoup

URL = "https://www.marmiton.org/recettes/recette-hasard.aspx?v=2"


class Recipe:

    class Ingredient:
        def __init__(self, name, quantity, unit):
            self.name = name
            self.quantity = quantity
            self.unit = unit
        
        def __str__(self):
            out = f"{self.name}"

            if self.quantity:
                out += f" : {self.quantity}"

            if self.unit:
                out += f" {self.unit}"

            return out

    class Step:
        def __init__(self, position, text):
            self.position = position
            self.text = text

        def __str__(self):
            return f"{self.position}. {self.text}"

    def fetch(self):
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        recipe = soup.find(id="__NEXT_DATA__").string
        recipe = json.loads(recipe)

        recipe = recipe["props"]["pageProps"]["recipeData"]["recipe"]

        self.title = recipe["title"]
        self.cookingTime = recipe["cookingTime"] // 60
        self.preparationTime = recipe["preparationTime"] // 60
        self.totalTime = recipe["totalTime"] // 60

        self.difficulty = recipe["difficulty"]["name"]
        self.dishType = recipe["dishType"]["name"]

        self.authorNotes = recipe["authorNotes"]

        self.servingsCount = recipe["servings"]["count"]
        self.servingsUnit = recipe["servings"]["unit"]

        self.ingredients = []
        for group in recipe["ingredientGroups"]:
            for ingredient in group["items"]:
                name = ingredient["name"]

                quantity = ingredient["ingredientQuantity"]
                unit = ingredient["unitName"] # unitPlural exist too

                self.ingredients.append(self.Ingredient(name, quantity, unit))

        self.steps = []
        for step in recipe["steps"]:
            position = step["position"] # assuming steps are already ordered
            text = step["text"] 
            self.steps.append(self.Step(position, text))

        return self

    def __str__(self):
        separation = "---------------------\n"
        sectionEnd = "\n"

        out =  "```"
        out += f"{self.title}\n"
        out += sectionEnd

        out += f"Informations\n"
        out += separation
        out += f"{self.dishType}\n"
        out += f"{self.servingsCount} {self.servingsUnit}\n"
        out += f"\n"
        out += f"Preparation : {self.preparationTime} minutes\n"
        out += f"Cuisson : {self.cookingTime} minutes\n"
        out += f"Temps Total : {self.totalTime} minutes\n"
        out += f"\n"
        out += f"Difficulté : {self.difficulty}"
        out += f"\n"

        if self.authorNotes and not "instagram" in self.authorNotes :
            out += f"Notes : {self.authorNotes}\n"
        out += sectionEnd

        out += f"Ingrédients\n"
        out += separation
        for ingredient in self.ingredients:
            out += f" - {ingredient}\n"
        out += sectionEnd

        out += f"Étapes\n"
        out += separation
        for step in self.steps:
            out += f" - {step}\n"
        out += sectionEnd
        out += "```"

        return out


if __name__ == "__main__":
    recipe = Recipe().fetch()
    print(recipe)