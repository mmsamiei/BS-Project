# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
from scrapy.conf import settings
import time
import re


class JavabyabspiderSpider(scrapy.Spider):
    name = 'javabyabSpider'
    allowed_domains = ['javabyab.com']
    start_urls = ['http://javabyab.com/']

    def __init__(self):
            connection = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
            db = connection[settings['MONGODB_DB']]
            self.collection = db[settings['MONGODB_COLLECTION']]  
    
    def start_requests(self):
            urls = [
                'https://javabyab.com/questions'
            ]
            first_questions = 'https://javabyab.com/questions'
            yield scrapy.Request(url=first_questions, callback=self.questions_page)

    def questions_page(self, response):
        questions_links = response.xpath('//*[contains(@class, "qa-q-item-title")]//@href').extract()
        for question_link in questions_links:
            question_absolute_link = response.urljoin(question_link)
            yield scrapy.Request(url=question_absolute_link, callback=self.question_page)
        next_page_link = response.xpath('//*[contains(@class, "qa-page-next")]/@href').extract_first()
        if next_page_link is not None:
            next_page_absolute_link = response.urljoin(next_page_link)
            yield scrapy.Request(url=next_page_absolute_link, callback=self.questions_page)

    def question_page(self, response):
        question_title = response.xpath('//*[contains(@class, "entry-title")]/text()').extract_first() 
        question_body = ' '.join(response.xpath('//*[contains(@class, "qa-q-view-content")]/div[contains(@class, "entry-content")]//text()').extract())
        question_body = question_body.replace('\n', ' ')
        question_url = response.request.url
        question_body = re.sub(' +', ' ', question_body)
        question_body = " ".join(question_body.split())
        if question_body == question_title:
            question_body = ""
        yield{
            'title': question_title,
            'body': question_body,
            'url': question_url,
            'checked': False
        }