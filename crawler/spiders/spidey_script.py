# -*- coding: utf-8 -*-
import scrapy
import urllib
from bs4 import BeautifulSoup 
from pymongo import MongoClient
from scrape_recipe import pprinty, parse_recipe


class RecipeSpiderSpider(scrapy.Spider):
    name = 'spidey_script'
    start_urls = ['https://www.tasteofhome.com/recipes/']
    #start_urls = ['https://www.maangchi.com/recipes']
    client = MongoClient()
    db = client.recipe_db_test
    recipe_collection = db.recipes

    def parse(self, response):
        urls = []
        html = BeautifulSoup(response.body, 'html.parser')
        for link in html.find_all('a'):
            url = link['href']
            if (url):
                url = urllib.parse.urljoin(response.url, url)
                if (url not in urls):
                    recipe = parse_recipe(url)
                    if (recipe):
                        pprinty(recipe)
                    urls.append(url)

