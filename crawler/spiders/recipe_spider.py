# -*- coding: utf-8 -*-
import scrapy
import scrape_recipe


class RecipeSpiderSpider(scrapy.Spider):
    name = 'recipe_spider'
    allowed_domains = ['https://www.tasteofhome.com/recipes/']
    start_urls = ['http://https://www.tasteofhome.com/recipes//']

    def parse(self, response):
        pass
