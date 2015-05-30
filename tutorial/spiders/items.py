# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class proItem(scrapy.Item):
    proname = scrapy.Field()
    link = scrapy.Field()

class yiyuanItem(scrapy.Item):
    proname = scrapy.Field()
    # cityname = scrapy.Field()
    yiyuanname = scrapy.Field()
    yiyuanlink = scrapy.Field()
    yiyuandesc = scrapy.Field()
    yiyuanaddress = scrapy.Field()
    yiyuantel = scrapy.Field()

class keshiItem(scrapy.Item):
    yiyuanname = scrapy.Field()
    keshiname = scrapy.Field()
    keshidesc = scrapy.Field()
    zhuanjialink = scrapy.Field()
    keshiparentname = scrapy.Field()
    keshijibinglink = scrapy.Field()

class zhuanjiaItem(scrapy.Item):
    zhuanjianame = scrapy.Field()
    yiyuanname = scrapy.Field()
    keshiname = scrapy.Field()
    zhuanjiatel = scrapy.Field()
    zhuanjiadesc = scrapy.Field()

class jibingItem(scrapy.Item):
    jibingname = scrapy.Field()
    jibinglink = scrapy.Field()
    jibingparentname = scrapy.Field()
