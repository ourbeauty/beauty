# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BeautyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    c_name = scrapy.Field()
    c2_name = scrapy.Field()
    g_name = scrapy.Field()
    g_desc = scrapy.Field()
    g_info = scrapy.Field()
    g_mktprice = scrapy.Field()
    g_price = scrapy.Field()
    g_goodprops = scrapy.Field()
    g_pics = scrapy.Field()
    g_class = scrapy.Field()

