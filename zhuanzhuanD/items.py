# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ZhuanzhuandItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    price = scrapy.Field()
    realPayPrice = scrapy.Field()
    file_paths = scrapy.Field()
    cutPrice = scrapy.Field()
    model = scrapy.Field()
    mainImg = scrapy.Field()

