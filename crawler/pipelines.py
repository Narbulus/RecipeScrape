# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from recipe_parser import pprinty

class PrintRecipePipeline(object):
    def process_item(self, item, spider):
        if spider.debug:
            pprinty(item)
        return item

class MongoPipeline(object):
    def close_spider(self, spider):
        spider.client.close()

    def process_item(self, item, spider):
        if spider.debug:
            print("Writing to MongoDB")
        spider.mongo.insert_one(dict(item))
        return item
