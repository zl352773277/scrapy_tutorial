#!/usr/bin/python
#coding:utf-8
__author__ = 'zhaolei'
import scrapy
import  sys
reload(sys)
sys.setdefaultencoding("utf-8")
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
from tutorial.items import proItem,yiyuanItem,keshiItem,zhuanjiaItem

class DmozSpider(scrapy.spider.Spider):
    name = "jibing"
    allowed_domains = ["haodf.com"]
    start_urls = [
        "http://www.haodf.com/jibing/neike/list.htm"
    ]


    def parse(self, response):
        for sel in response.xpath('//div[@class="jeshi_tree"]/div/div/a'):
            keshiitem = keshiItem()
            keshiitem['keshiname'] = sel.xpath('text()').extract()[0].decode("utf-8")
            keshiitem['keshijibinglink'] = sel.xpath('@href').extract()[0].decode("utf-8")
            print keshiitem['keshiname'] + keshiitem['keshijibinglink']
            # with open("province", 'a') as f:
            #     f.write(""proitem['proname'] + proitem['link']+"\n")
            # proitems.append(proitem)
            # self.make_requests_from_url(proitem['link']).replace(meta={'proitem':proitem},callback=self.parse_yiyuan)
            yield Request('http://www.haodf.com'+keshiitem['keshijibinglink'],meta={'keshiitem':keshiitem},callback=self.parse_jibing)
        # return proitems

    def parse_jibing(self, response):
        for sel in response.xpath('//div[@class="jeshi_tree"]/div/div/ul/li/a'):
            # keshiitem = keshiItem()
            # keshiitem['keshiname'] = sel.xpath('text()').extract()[0].decode("utf-8")
            # keshiitem['keshijibinglink'] = sel.xpath('@href').extract()[0].decode("utf-8")
            print sel.xpath('text()').extract()[0].decode("utf-8") + sel.xpath('@href').extract()[0].decode("utf-8")
            # with open("province", 'a') as f:
            #     f.write(""proitem['proname'] + proitem['link']+"\n")
            # proitems.append(proitem)
            # self.make_requests_from_url(proitem['link']).replace(meta={'proitem':proitem},callback=self.parse_yiyuan)
            yield Request('http://www.haodf.com'+sel.xpath('@href').extract()[0].decode("utf-8"),callback=self.parse_jibing_child)

    def parse_jibing_child(self, response):
        for sel in response.xpath('//div[@class="ct"]/div/ul/li/a'):
            # keshiitem = keshiItem()
            # keshiitem['keshiname'] = sel.xpath('text()').extract()[0].decode("utf-8")
            # keshiitem['keshijibinglink'] = sel.xpath('@href').extract()[0].decode("utf-8")
            print sel.xpath('text()').extract()[0].decode("utf-8") + sel.xpath('@href').extract()[0].decode("utf-8")
            # with open("province", 'a') as f:
            #     f.write(""proitem['proname'] + proitem['link']+"\n")
            # proitems.append(proitem)
            # self.make_requests_from_url(proitem['link']).replace(meta={'proitem':proitem},callback=self.parse_yiyuan)
            # yield Request('http://www.haodf.com'+sel.xpath('@href').extract()[0].decode("utf-8"),callback=self.parse_jibing_child)

