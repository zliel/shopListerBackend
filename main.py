import re

from urllib.parse import urlparse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup as bs

app = FastAPI()
origins = ["http://localhost:3000"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"])


@app.get("/scrape")
def scrape_recipe(url: str):
    """This endpoint scrapes the ingredients from the linked recipe """
    # Validate the url
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return {"error": "Invalid URL"}

    # If the url is valid, scrape the recipe
    page = requests.get(url)
    soup = bs(page.content, "html.parser")
    recipe_name = soup.select_one("h2 .wprm-recipe-name").text
    soup_ingredients = soup.find_all("li", class_="wprm-recipe-ingredient")
    result_ingredients = []

    for ingredient in soup_ingredients:
        amount = ingredient.find("span", class_=re.compile(r"amount"))
        amount_text = amount.text if amount is not None else ""
        unit = ingredient.find("span", class_=re.compile(r"unit"))
        unit_text = unit.text if unit is not None else ""
        name = ingredient.find("span", class_=re.compile(r"name"))
        name_text = name.text if name is not None else ""

        result_ingredients.append(f"{amount_text} {unit_text} {name_text}")

    # We send back the page.url because the JOC page autocompletes incomplete urls to the closest matching recipe
    return {"name": recipe_name, "ingredients": result_ingredients, "url": page.url}
