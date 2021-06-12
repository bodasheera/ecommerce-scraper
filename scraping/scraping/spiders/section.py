from ..components.navigation import get_navigation
from typing import List
from scrapy.spiders import Spider
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from ..components import entity as e
from ..components import element_locators as el
import scrapy
import pandas as pd
import json
import time 
from datetime import datetime
from cryptography.fernet import Fernet 
now = datetime.now()
d1 = now.strftime("%d/%m/%Y %H:%M:%S")


class Section(Spider):
        name = 'section'
        section_name : str;        
        description: str;
        base_path : any;
        id: int;
        parent_id : int;
        base_url: str;
        # start_urls = []
        entityList: List;
        pagination: str; 
        final_data: List;
        add_base_url: List;
        file: str;
        page_data_count : int;


        def __init__(self, message, key):
            message = message.encode('utf-8')
            key = key.encode('utf-8')
            fernet = Fernet(key) 
            data = fernet.decrypt(message).decode() 
            data = json.loads(data)
            path = data['path']
            self.base_path = (el.Switcher(path['type']).get_class())(path['value'])
            self.section_name = data['name']
            self.description = data['description']
            self.id = data['id']
            self.parent_id = data['parent_id']
            self.base_url = data['base_url']
            self.start_urls = data['start_urls'][0:5]
            self.set_pagination(data['pagination'])
            self.entityList = []
            self.final_data = []
            self.insert_entities(data['entities'])
            self.add_base_url = data['add_base_url']
            self.file = data['file']
            self.page_data_count = 0


        def set_pagination(self, pagination):
            pagination = pagination
            if pagination['value'] is not None:
                self.pagination = get_navigation(el.Switcher(pagination['type']).get_class())(pagination['value'], pagination['route'])
            else:
                self.pagination = None


        def insert_entities(self,entities):
            for entity in entities:
                s = el.Switcher(entity['type'])
                entity_object = (e.get_entity(s.get_class()))(entity['name'], entity['value'])
                self.entityList.append(entity_object)


        def parse(self, response):
            self.page_data_count = 0
          

            for data in self.base_path.get_html(response):
                result = {}
                result['start_url'] = response.url
               
                result['timestamp'] = d1
                for entity in self.entityList:
                    
                    if entity.get(data) is not None and entity.name in self.add_base_url:
                        value = self.base_url + entity.get(data)
                    else:
                        value = entity.get(data)
                   
                    result[entity.name] = value.strip() if value is not None else None

                # yield result
                self.final_data.append(result)
                self.page_data_count += 1
                result = {}

            if self.pagination is not None and self.page_data_count > 0 and len(self.final_data) < 100:
                next_page = self.pagination.get(response)

                if next_page is not None:
                    if 'http' not in next_page:
                        next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)


        @classmethod
        def from_crawler(cls, crawler, *args, **kwargs):
            spider = super(Section, cls).from_crawler(crawler, *args, **kwargs)
            crawler.signals.connect(spider.spider_closed, signal=scrapy.signals.spider_closed)
            return spider


        def spider_closed(self, spider):
            spider.logger.info('Spider closed')
            df = pd.DataFrame.from_records(self.final_data)
            df.to_csv('scraping/output/' + self.file + '.csv', index= False, encoding='utf-8-sig')
            