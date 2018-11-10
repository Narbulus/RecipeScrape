# -*- coding: utf-8 -*-
import scrapy
import scrape_recipe
import urllib
from bs4 import BeautifulSoup 
from pymongo import MongoClient


class RecipeSpiderSpider(scrapy.Spider):
    name = 'recipe_spider'
    #start_urls = ['https://www.tasteofhome.com/recipes/']
    start_urls = ['https://www.maangchi.com/recipes']
    client = MongoClient()
    db = client.recipe_db_test
    recipe_collection = db.recipes

    def parse(self, response):
        urls = []
        print(response.url)
        html = BeautifulSoup(response.body, 'html.parser')
        for link in html.find_all('a'):
            url = link['href']
            if (url):
                url = urllib.parse.urljoin(response.url, url)
                if (url not in urls):
                    print("Parsing URL " + url)
                    scrape_recipe.parse_recipe(url)
                    urls.append(url)
        
