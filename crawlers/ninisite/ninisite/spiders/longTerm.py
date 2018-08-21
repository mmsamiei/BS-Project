# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
from scrapy.conf import settings
import time


class LongtermSpider(scrapy.Spider):
    name = 'longTerm'
    # allowed_domains = ['www.ninisite.com']
    # start_urls = ['http://www.ninisite.com/']

    def __init__(self):
        connection = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def start_requests(self):
        category_page = 'https://www.ninisite.com/discussion'
        yield scrapy.Request(url=category_page, callback=self.categories_page)
    
    def categories_page(self, response):
        category_links = response.xpath('//*[contains(@class, "category--title")]/@href').extract()
        url_to_join = 'https://www.ninisite.com'
        for category_link in category_links:
            category_absolute_link = response.urljoin(category_link)
            yield scrapy.Request(url=category_absolute_link, callback=self.short_term_page)


    def short_term_page(self, response):
        topic_links = response.xpath('//*[contains(@class, "topic--title")]/../@href').extract()
        for topic_link in topic_links:
            topic_absolute_link = response.urljoin(topic_link)
            yield scrapy.Request(url=topic_absolute_link, callback=self.parse_topic_page)
        next_page_link = response.xpath('//*[contains(@class, "page-link")][@title="Next page"]/@href').extract_first()
        if next_page_link is not None:
            next_page_absolute_link = response.urljoin(next_page_link)
            yield scrapy.Request(url=next_page_absolute_link, callback=self.short_term_page)
    
    def parse_topic_page(self, response):
        topic_title = response.xpath('//*[contains(@class, "topic-title")]/a/text()').extract_first() 
        main_post_message = response.xpath('//*[contains(@class, "post-message")]')[0]
        main_post_message_text = ' '.join(main_post_message.xpath('./p/text()').extract())
        topic_url = response.request.url
        yield{
            'title': topic_title,
            'body': main_post_message_text,
            'url': topic_url,
            'checked': False
        }
