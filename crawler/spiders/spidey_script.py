# -*- coding: utf-8 -*-
import scrapy
import urllib
from pymongo import MongoClient
from bs4 import BeautifulSoup 
from recipe_parser import parse_recipe

DEFAULT_RECIPE_URL = 'https://www.tasteofhome.com/recipes/'

class RecipeSpiderSpider(scrapy.Spider):
    name = 'spidey_script'

    def __init__(self, db_name="spidey_data", *args, **kwargs):
        super(RecipeSpiderSpider, self).__init__(*args, **kwargs)
        client = MongoClient()
        db = client[db_name]
        self.mongo = db["recipes"]

    def start_requests(self):
        if hasattr(self, 'url'):
            yield scrapy.Request(self.url)
        yield scrapy.Request(DEFAULT_RECIPE_URL)

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
                        yield recipe
