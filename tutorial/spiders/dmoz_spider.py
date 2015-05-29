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
    name = "dmoz"
    allowed_domains = ["haodf.com"]
    start_urls = [
        "http://www.haodf.com/yiyuan/beijing/list.htm"
    ]


    def parse(self, response):
        proitems = []
        for sel in response.xpath('//div[@class="jeshi_tree"]/div/div/a'):
            proitem = proItem()
            proitem['proname'] = sel.xpath('text()').extract()[0].decode("utf-8")
            proitem['link'] = sel.xpath('@href').extract()[0].decode("utf-8")
            # print proitem['proname'] + proitem['link']
            # with open("province", 'a') as f:
            #     f.write(""proitem['proname'] + proitem['link']+"\n")
            proitems.append(proitem)
            # self.make_requests_from_url(proitem['link']).replace(meta={'proitem':proitem},callback=self.parse_yiyuan)
            yield Request(proitem['link'],meta={'proitem':proitem},callback=self.parse_yiyuan)
        # return proitems

    def parse_yiyuan(self,response):
        yiyuanItems = []
        i = 1
        for sel in response.xpath('//div[@class="m_ctt_green"]/ul/li/a'):
            yiyuanitem = yiyuanItem()
            yiyuanitem['proname'] = response.meta['proitem']['proname']
            yiyuanitem['yiyuanname'] = sel.xpath('text()').extract()[0].decode("utf-8")
            yiyuanitem['yiyuanlink'] = sel.xpath('@href').extract()[0].decode("utf-8")
            yiyuanitem['yiyuancode'] = i  #自己生成医院编号，从1开始
            i+=1
            # print yiyuanitem['yiyuanname'] + yiyuanitem['yiyuanlink']
            yiyuanItems.append(yiyuanitem)
            yield Request("http://www.haodf.com" + yiyuanitem['yiyuanlink'].decode("utf-8"),meta={'yiyuanitem':yiyuanitem},callback=self.parse_yiyuan_detail)
            

    def parse_yiyuan_detail(self,response):
        yiyuanitem = response.meta['yiyuanitem']

        sel = response.xpath("//table[@id='hosabout']//tr")
        yiyuanitem['yiyuantel'] = ""
        for s in sel:
            if len(s.xpath("./td[2]/nobr/text()").extract()) != 0:
                if u'\u533b\u9662\u4ecb\u7ecd\uff1a' == s.xpath("./td[2]/nobr/text()").extract()[0] or u'\u5c31\u533b\u6307\u5357\uff1a' == s.xpath("./td[2]/nobr/text()").extract()[0] :
                    yiyuanitem['yiyuandesc'] = s.xpath("./td[2]/text()").extract()[0].decode("utf-8")
                    print yiyuanitem['yiyuandesc']
                elif u'\u5730\u3000\u3000\u5740\uff1a' == s.xpath("./td[2]/nobr/text()").extract()[0]:
                    yiyuanitem['yiyuanaddress'] = s.xpath("./td[2]/text()").extract()[0].decode("utf-8")
                    print yiyuanitem['yiyuanaddress']
                elif u'\u7535\u3000\u3000\u8bdd\uff1a' == s.xpath("./td[2]/nobr/text()").extract()[0]:
                    yiyuanitem['yiyuantel'] = s.xpath("./td[2]/text()").extract()[0].decode("utf-8")
                    print yiyuanitem['yiyuantel']

            # href = sel.xpath('@href').extract()
        with open("yiyuan.sql", 'a') as f:
            f.write("INSERT INTO tbHospital(code,name,introduce,address,tel) VALUES ('%s','%s','%s','%s','%s');" %(yiyuanitem['yiyuancode'],yiyuanitem['yiyuanname'],yiyuanitem['yiyuandesc'],yiyuanitem['yiyuanaddress'],yiyuanitem['yiyuantel'])+"\n")

        sel_keshies =response.xpath('//td[@width="50%"]')
        i = 1
        for sel in sel_keshies:
            keshiitem = keshiItem()
            keshiitem['keshicode'] = i
            i+=1  #自己生成科室code
            keshiitem['yiyuancode'] = yiyuanitem['yiyuancode']
            keshiitem['keshiname'] = sel.xpath('a/text()').extract()[0].decode("utf-8")
            keshiitem['zhuanjialink'] = sel.xpath('a/@href').extract()[0].decode("utf-8")
            with open("keshi.sql", 'a') as f:
                f.write("INSERT INTO tbBranchs(code,name,hCode) VALUES ('%s','%s','%s');" %(keshiitem['keshicode'],keshiitem['keshiname'],keshiitem['yiyuancode']) + "\n")
            yield Request(keshiitem['zhuanjialink'],meta={'keshiitem':keshiitem},callback=self.parse_zhuanjia)

    def parse_zhuanjia(self,response):
        keshiitem = response.meta['keshiitem']
        # print response.xpath('//*[@id="doc_list_index"]').xpath(".//tr").extract()
        i= 0
        for sel in response.xpath('//*[@id="doc_list_index"]').xpath(".//tr"):
            zhuanjiaitem = zhuanjiaItem()
            zhuanjiaitem['zhuanjiacode'] = i
            i+=1  #自己生成专家code
            zhuanjiaitem['zhuanjiakeshicode'] = str(keshiitem['yiyuancode'])+'-'+str(keshiitem['keshicode'])
            #zhuanjiaitem['keshiname'] = keshiitem['keshiname']
            #zhuanjiaitem['yiyuanname'] = keshiitem['yiyuanname']
            # zhuanjiaitem['zhuanjianame'] = sel.xpath('.//td[1]/li/a/text()').extract()[0].decode('utf-8')
            # zhuanjiaitem['zhuanjiashanchang'] = sel.xpath('.//td[2]/text()').extract()[0].decode('utf-8')
            if len(sel.xpath('.//td[1]/li').extract()) != 0:
                zhuanjiaitem['zhuanjianame'] = sel.xpath('.//td[1]/li/a/text()').extract()[0].decode('utf-8')
                zhuanjiaitem['zhuanjiashanchang'] = sel.xpath('.//td[2]/text()').extract()[0].decode('utf-8')
                with open("zhuanjia.sql", 'a') as f:
                    f.write("INSERT INTO tbExperts(code,name,branchCode,specialty) VALUES ('%s','%s','%s','%s');" %(zhuanjiaitem['zhuanjiacode'],zhuanjiaitem['zhuanjianame'],zhuanjiaitem['zhuanjiakeshicode'],zhuanjiaitem['zhuanjiashanchang']) + "\n")
            # yield Request(href[0].decode("utf-8"),callback=self.parse_keshi_detail)
    # #
    # def parse_keshi_detail(self,response):
    #     for sel in response.xpath('//div[@class="m_ctt_green"]/ul/li/a'):
    #         title = sel.xpath('text()').extract()
    #         href = sel.xpath('@href').extract()
    #         with open("yiyuan", 'w+') as f:
    #             f.write(title[0].decode("utf-8") + href[0].decode("utf-8"))
    #         print title[0].decode("utf-8") + href[0].decode("utf-8")
    #         yield Request(href[0].decode("utf-8"),callback=self.parse_zhuanjia)
    #
    # def parse_zhuanjia(self,response):
    #     for sel in response.xpath('//div[@class="m_ctt_green"]/ul/li/a'):
    #         title = sel.xpath('text()').extract()
    #         href = sel.xpath('@href').extract()
    #         with open("yiyuan", 'w+') as f:
    #             f.write(title[0].decode("utf-8") + href[0].decode("utf-8"))
    #         print title[0].decode("utf-8") + href[0].decode("utf-8")
    #         yield Request(href[0].decode("utf-8"),callback=self.parse_zhuanjia_detail)
    #
    # def parse_zhuanjia_detail(self,response):
    #     for sel in response.xpath('//div[@class="m_ctt_green"]/ul/li/a'):
    #         title = sel.xpath('text()').extract()
    #         href = sel.xpath('@href').extract()
    #         with open("yiyuan", 'w+') as f:
    #             f.write(title[0].decode("utf-8") + href[0].decode("utf-8"))
    #         print title[0].decode("utf-8") + href[0].decode("utf-8")
    #         yield Request(href[0].decode("utf-8"),callback=self.parse_zhuanjia_detail)