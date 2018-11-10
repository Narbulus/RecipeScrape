# -*- coding: utf-8 -*-
import scrapy
import urllib
from bs4 import BeautifulSoup 
from pymongo import MongoClient
from recipe_parser import pprinty, parse_recipe


class RecipeSpiderSpider(scrapy.Spider):
    name = 'spidey_script'
    client = MongoClient()
    db = client.recipe_db_test
    recipe_collection = db.recipes

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse(self, response):
        urls = []
        html = BeautifulSoup(response.body, 'html.parser')
        for link in html.find_all('a'):
            url = link['href']
            if (url):
                url = urllib.parse.urljoin(response.url, url)
                if (self.debug):
                    print(url)
                if (url not in urls):
                    urls.append(url)
                    recipe = parse_recipe(url, self.debug)
                    if (recipe):
                        if (self.debug):
                            pprinty(recipe)
                        yield recipe

