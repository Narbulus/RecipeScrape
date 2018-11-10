# -*- coding: utf-8 -*-
import scrapy
import urllib
from bs4 import BeautifulSoup 
from pymongo import MongoClient
from scrape_recipe import pprinty, parse_recipe


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
                    pprinty(parse_recipe(recipe_url))
                    urls.append(url)
        
