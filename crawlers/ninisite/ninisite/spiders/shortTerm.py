# -*- coding: utf-8 -*-
import scrapy


class ShorttermSpider(scrapy.Spider):
    name = 'shortTerm'
    allowed_domains = ['www.ninisite.com']
    start_urls = ['http://www.ninisite.com/']

    def parse(self, response):
        pass
