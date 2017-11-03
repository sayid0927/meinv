# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyfendoItem(scrapy.Item):
    # define the fields for your item here like:

    dir = scrapy.Field()
    title = scrapy.Field()
    imgUrl = scrapy.Field()
    img_name = scrapy.Field()
