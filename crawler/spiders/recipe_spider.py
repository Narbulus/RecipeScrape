# -*- coding: utf-8 -*-
import scrapy
import scrape_recipe
from bs4 import BeautifulSoup 


class RecipeSpiderSpider(scrapy.Spider):
    name = 'recipe_spider'
    start_urls = ['https://www.tasteofhome.com/recipes/']

    def parse(self, response):
        print(response.url)
        html = BeautifulSoup(response.body, 'html.parser')
        for recipe_item in html.find_all('li'):
            for recipe_link in recipe_item.find_all('a'):
                recipe_url = recipe_link['href']
                if (recipe_url):
                    print("FOUND ONE " + recipe_url)
                    #scrape_recipe.parse_recipe(recipe_url)
        
