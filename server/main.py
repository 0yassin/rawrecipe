from fastapi import HTTPException
from parser import Ingredient_parser
from fastapi import FastAPI
from scraper import Ldscraper
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

parser = Ingredient_parser()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)


@app.get('/scrape_recipe')
def scrape_recipe(url:str):

    if not url:
        raise HTTPException(status_code=400, detail="Missing url query parameter")


    scraper = Ldscraper(url)
    if scraper.fetch():
        recipe = scraper.get_recipe()
        return recipe


    raise HTTPException(status_code=404, detail="Could not find schema recipe data at provided URL")    