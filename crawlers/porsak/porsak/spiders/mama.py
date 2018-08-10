# -*- coding: utf-8 -*-
import scrapy


class MamaSpider(scrapy.Spider):
    name = 'mama'
    allowed_domains = ['http://porsak.ir']
    start_urls = ['http://http://porsak.ir/']

    def parse(self, response):
        pass
