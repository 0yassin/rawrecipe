from scraper import Ldscraper
scraper = Ldscraper("https://sallysbakingaddiction.com/chewy-chocolate-chip-cookies/")

if scraper.fetch():
    recipe = scraper.get_recipe()
    print(scraper.get_recipe()["ingredients"])