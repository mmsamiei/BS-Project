# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
from scrapy.conf import settings
import time


class ShortermSpider(scrapy.Spider):
    name = 'shortTerm'
    # allowed_domains = ['www.ninisite.com']
    # start_urls = ['http://www.ninisite.com/']

    def __init__(self):
        connection = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def start_requests(self):
        urls = [
            'https://www.ninisite.com/discussion/'
        ]
        short_term_topics = 'https://www.ninisite.com/discussion/topics'
        yield scrapy.Request(url=short_term_topics, callback=self.short_term_page)
    
    def short_term_page(self, response):
        topic_links = response.xpath('//*[contains(@class, "topic--title")]/../@href').extract()
        for topic_link in topic_links:
            topic_absolute_link = response.urljoin(topic_link)
            if self.collection.find_one({'url':topic_absolute_link}) is None:
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
            'checked': 0
        }
