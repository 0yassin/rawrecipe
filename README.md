# rawrecipe

An app designed to extract clean recipe data from bloated recipe websites that are full of ads and trackers *(which are definitely not there because of a certain company starting with G and ending in OOGLE)*.

---

## Current Tech Stack

* **Frontend:** Next.js
* **Backend:** FastAPI
* **Scraping:** Beautiful Soup 4 (`bs4`)

---

## Demo:
- you can visit the [website](https://rawrecipe.netlify.app/)
---
## How you can run it locally
### First setup the server
- Step 1: clone the repo:
    ```git clone https://github.com/0yassin/rawrecipe.git```
- Step 2: navigate into the server folder: ```cd rawrecipe/server```
- Step 3: create a venv envirement: ```python -m venv venv``` 
- Step 4: activate your envirement: ```source venv/bin/activate``` (or if you're on windows: ```venv\Scripts\activate```)
- Step 5: install dependancies: ```pip install -r requirements.txt```
- Step 6: run the python server: ```uvicorn main:app --reload --port 8000``` (this will run the server on localhost:8000)
### Now run the frontend
- Step 1: navigate to the frontend folder: ```cd ../rawrecipe-website```
- Step 2: install dependancies: ```npm install```
- Step 3: create a .env file: ```echo "NEXT_PUBLIC_API_URL=localhost:8000" > .env.local``` 
- note: If you are on Windows CMD, manually create a file named ```.env.local``` (in the rawrecipe-website) directory and add ```NEXT_PUBLIC_API_URL=localhost:8000``` inside it, if you changed the uvicorn settings earlier you must use them here too.
- Step 4: run the app ```npm run dev```
- Step 5: open [localhost:3000](http://localhost:3000) and enjoy!
---
## Future Features

* [ ] Built-in unit conversion
* [ ] Command Line Interface (CLI) version
* [ ] A better way of displaying the recipes on the website
* [ ] More customizations and themes
* [ ] Maybe a better, less stupid name for the project

---

> Thank you for reading this!