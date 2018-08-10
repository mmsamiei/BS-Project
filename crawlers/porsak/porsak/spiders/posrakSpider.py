# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
from scrapy.conf import settings
import time


class PosrakspiderSpider(scrapy.Spider):
    name = 'porsakSpider'
    #allowed_domains = ['http://porsak.ir']
    #start_urls = ['http://http://porsak.ir/']

    def __init__(self):
        connection = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
    
    def start_requests(self):
        urls = [
            'http://porsak.ir/?qa=questions'
        ]
        first_questions = 'http://porsak.ir/?qa=questions'
        yield scrapy.Request(url=first_questions, callback=self.questions_page)

    def questions_page(self, response):
        questions_links = response.xpath('//*[contains(@class, "qa-q-item-title")]//@href').extract()
        for question_link in questions_links:
            question_absolute_link = response.urljoin(question_link)
            yield scrapy.Request(url=question_absolute_link, callback=self.question_page)

    def question_page(self, response):
        question_title = response.xpath('//*[contains(@class, "entry-title")]/text()').extract_first() 
        question_body = ' '.join(response.xpath('//*[contains(@class, "qa-q-view-content")]/div[contains(@class, "entry-content")]//text()').extract())
        print("**********************************")
        question_body = question_body.replace('\n', ' ')
        print("question body is :" + str(question_body))
        print("**********************************")