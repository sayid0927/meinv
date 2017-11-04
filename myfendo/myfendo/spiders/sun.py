# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from myfendo.items import MyfendoItem

from scrapy_redis.spiders import RedisCrawlSpider

import sys
reload(sys)
sys.setdefaultencoding('utf8')

# class SunSpider(CrawlSpider):
class SunSpider(RedisCrawlSpider):
    name = 'sun'
    allowed_domains = ['meinvha.com']
    # start_urls = ['http://www.meinvha.com/xinggan/']

    home_url ='http://www.meinvha.com'
    nex_list ='http://www.meinvha.com/mote/'

    allowed_domains = ['meinvha.com']

    redis_key = 'sunspider:start_urls'

    def __int__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(SunSpider, self).__int__(*args, **kwargs)





    def parse(self, response):

        # 头像列表
        meinv_links = response.xpath('//ul[@class="clearfix"]/li/a/@href').extract()
        # # 头像封面
        # meinv_cover = response.xpath('//ul[@class="clearfix"]/li/a/img/@src').extract()
        # 下一页列表
        net_List = response.xpath('//div[@class="page"]/a/@href').extract()

        for link in net_List:

            yield scrapy.Request(self.nex_list+link, callback=self.parse)

        else:

            print  'net_List is NULL'


        for link in meinv_links:

            yield scrapy.Request(self.home_url+link,callback=self.process_item)

        else:

            print 'meinv_links is NULL'


    def process_item(self, response):



        dir = response.xpath('//div[@class="breadnav"]//a/text()').extract()[1]

        img_name  = response.xpath('//div[@class="picmainer"]/h1').extract()[0]

        title = response.xpath('//div[@class="picsbox picsboxcenter"]/p/a/img/@alt | //div[@class="picsbox picsboxcenter"]/p/img/@alt').extract()[0]


        net_List = response.xpath('//div[@class="page"]/a/@href').extract()

        img_url = response.xpath('//div[@class="picsbox picsboxcenter"]/p/a/img/@src | //div[@class="picsbox picsboxcenter"]/p/img/@src').extract()


        for link in net_List:

            yield scrapy.Request(self.nex_list+link, callback=self.process_item)

        else:

            print  'net_List is NULL'



        img_name = re.findall(r"[0-9]", img_name)

        if len(img_name) == 0:
            img_name = 0
        else:
            s = ''
            for i in img_name:
                s += i
            img_name = s

        i = MyfendoItem()
        i['title'] = title
        i['imgUrl'] = img_url
        i['dir'] = dir
        i['img_name'] = img_name

        yield i

