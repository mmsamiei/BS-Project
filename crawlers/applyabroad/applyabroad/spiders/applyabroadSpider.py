# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
from scrapy.conf import settings
import time


class ApplyabroadspiderSpider(scrapy.Spider):
    name = 'applyabroadSpider'
    #allowed_domains = ['applyabroad.org']
    #start_urls = ['http://applyabroad.org/']

    def __init__(self):
        connection = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        print("1")

    def start_requests(self):
        topics = 'https://www.applyabroad.org/forum/archive/index.php'
        yield scrapy.Request(url=topics, callback=self.topics_page)
        print("2")

    def topics_page(self, response):
        topics_link = response.xpath('//div[@id="content"]//a/@href').extract()
        print(topics_link)
        for topic_link in topics_link:
            yield scrapy.Request(url=topic_link, callback=self.topic_page)
        print("3")

    def topic_page(self, response):
        posts_link = response.xpath('//div[@id="content"]//a/@href').extract()
        for post_link in posts_link:
            if self.collection.find_one({'url':post_link}) is None:
                yield scrapy.Request(url=post_link, callback=self.post_page)
            else:
                print("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
                break
        print("4")

    def post_page(self, response):
        post_body = ' '.join(response.xpath('//div[@class="posttext"]')[0].xpath('./text()').extract())
        post_title = response.xpath('//p[@class="largefont"]/a/text()').extract_first()
        post_url = response.request.url
        yield{
            'title': post_title,
            'body': post_body,
            'url': post_url,
            'checked': False
        }
        print("5")
            
