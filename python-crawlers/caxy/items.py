# -*- coding: utf-8 -*-

import scrapy


class CaxyItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    names = scrapy.Field()

