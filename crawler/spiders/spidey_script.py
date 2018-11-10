# -*- coding: utf-8 -*-
import scrapy
import urllib
from pymongo import MongoClient
from bs4 import BeautifulSoup 
from scrape_recipe import parse_recipe

DEFAULT_RECIPE_URL = 'https://www.tasteofhome.com/recipes/'

class RecipeSpiderSpider(scrapy.Spider):
    name = 'spidey_script'

    def __init__(self, db_name="spidey_data", debug=False, *args, **kwargs):
        super(RecipeSpiderSpider, self).__init__(*args, **kwargs)
        self.client = MongoClient()
        self.db = self.client[db_name]
        self.mongo = self.db["recipes"]
        if debug is False:
            self.debug = False
        else:
            self.debug = True

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
                    recipe = parse_recipe(url)
                    if (recipe):
                        yield recipe
