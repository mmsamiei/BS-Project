# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
from scrapy.conf import settings
import time
import re
from selenium import webdriver
import os
from scrapy.selector import Selector
from pyvirtualdisplay import Display

class TebyanspiderSpider(scrapy.Spider):
    name = 'tebyanSpider'
    #allowed_domains = ['https://moshavere.tebyan.net/']
    #start_urls = ['http://https://moshavere.tebyan.net//']

    def __init__(self):
        connection = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        #TODO
        #self.driver = webdriver.Firefox(executable_path='/home/mahdi/Public/BS_Project/crawlers/geckodriver')

    def start_requests(self):
        urls = [
            'https://www.tebyan.net/newindex.aspx?pid=851&GroupParentID=391',
            'https://www.tebyan.net/newindex.aspx?pid=851&GroupParentID=386',
            'https://www.tebyan.net/newindex.aspx?pid=851&GroupParentID=387',
            'https://moshavere.tebyan.net/newindex.aspx?pid=851&GroupParentID=1136'
        ]


        for url in urls:
            #self.driver.get(url)
            yield scrapy.Request(url=url, callback=self.questions_page)
        #self.driver.quit()


    def questions_page(self, response):
        display = Display(visible=0, size=(1024, 768))
        display.start()
        derive_path = '/root/mahdi/BS-Project/crawlers/geckodriver'
        #derive_path = '/home/mahdi/Public/Zirab/BS-Project/crawlers/geckodriver'
        driver = webdriver.Firefox(executable_path=derive_path)
        try:
            driver.get(response.request.url)
            sel = Selector(text = driver.page_source)
            last_question_link = sel.xpath('//*[contains(@class, "ConsultationQuestion")]//@href').extract()[-1]
            last_question_link = response.urljoin(last_question_link)
            repetition = False
            temp = self.collection.find_one({'url':last_question_link})
            if temp is not None:
                repetition = True
            i = 0 
            previous_question_link = last_question_link
            while(repetition is False):
                driver.find_element_by_xpath('//div[@id="__ConsultaionMore__"]').click()
                sel = Selector(text = driver.page_source)
                last_question_link = sel.xpath('//*[contains(@class, "ConsultationQuestion")]//@href').extract()[-1]
                last_question_link = response.urljoin(last_question_link)
                temp = self.collection.find_one({'url':last_question_link})
                if temp is not None or previous_question_link == last_question_link:
                    repetition = True
                i = i + 1
                print(last_question_link+" \t " + str(i))
                previous_question_link = last_question_link
            
            sel = Selector(text = driver.page_source)
            questions_links = sel.xpath('//*[contains(@class, "ConsultationQuestion")]//@href').extract()
            questions_bodies = sel.xpath('//*[contains(@class, "ConsultationQuestion")]/a/text()').extract()
            questions = sel.xpath('//*[contains(@class, "ConsultationQuestion")]/a')
            for question in questions:
                question_link = response.urljoin(question.xpath('./@href').extract_first())
                question_body = ' '.join(question.xpath('./text()').extract())
                yield{
                'title': "",
                'body': question_body,
                'url': question_link,
                'checked': False
                }
        except:
            pass
        driver.quit()
        display.stop()
            



