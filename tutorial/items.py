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
    yiyuancode = scrapy.Field()
    yiyuanname = scrapy.Field()
    yiyuanlink = scrapy.Field()
    yiyuandesc = scrapy.Field()
    yiyuanaddress = scrapy.Field()
    yiyuantel = scrapy.Field()

class keshiItem(scrapy.Item):
    yiyuancode = scrapy.Field()
    keshicode = scrapy.Field()
    keshiname = scrapy.Field()
    keshidesc = scrapy.Field()
    zhuanjialink = scrapy.Field()
    keshiparentname = scrapy.Field()

class zhuanjiaItem(scrapy.Item):
    zhuanjiacode = scrapy.Field()
    zhuanjiakeshicode = scrapy.Field()
    zhuanjianame = scrapy.Field()
    yiyuanname = scrapy.Field()
    keshiname = scrapy.Field()
    zhuanjiatel = scrapy.Field()
    zhuanjiashanchang = scrapy.Field()
