# -*- coding: utf-8 -*-
import itertools
import scrapy
import urllib
import re
from pymongo import MongoClient
from bs4 import BeautifulSoup 
from recipe_parser import parse_recipe
from scrapy_splash import SplashRequest

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
        url = DEFAULT_RECIPE_URL
        if hasattr(self, 'url'):
            url = self.url
        yield SplashRequest(url, self.parse_result, args={'wait': 0.5}, endpoint='render.html')

    def parse_result(self, response):
        urls = []
        for url in self.extract_link_urls(response):
            recipe = self.process_recipe_url(url, urls)
            if (recipe):
                yield recipe
    
    def extract_link_urls(self, response):
        html = BeautifulSoup(response.text, 'html.parser')
        # Check for recipes in the DOM first
        for link in html.find_all('a'):
            url = link.get('href')
            if (url) :
                if (self.debug):
                    print("Link URL: " + url)
                yield url

    def extract_raw_urls(self, response):
        # Check for raw URLs floating around (like in scripts)
        regexp = re.compile('\"(?:[-:\/\w.]|(?:%[\da-fA-F]{2}))+(?:\/[-\w]+)*\/?\"')
        raw_urls = regexp.findall(response.text)
        for url in raw_urls:
            if (self.debug):
                print("Raw URL: " + url)
            yield url
                
    def process_recipe_url(self, url, seen_urls):
        if (url not in seen_urls and 'recipe' in url):
            seen_urls.append(url)
            recipe = parse_recipe(url, self.debug)
            if (recipe):
                return recipe
