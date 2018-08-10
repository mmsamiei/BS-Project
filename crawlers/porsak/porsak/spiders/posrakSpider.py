# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
from scrapy.conf import settings
import time


class PosrakspiderSpider(scrapy.Spider):
    name = 'posrakSpider'
    allowed_domains = ['http://porsak.ir']
    start_urls = ['http://http://porsak.ir/']

    def parse(self, response):
        pass
