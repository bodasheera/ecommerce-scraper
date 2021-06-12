import os
from typing import List

from scrapy.cmdline import execute
import json
from cryptography.fernet import Fernet 

from configs import base_config as bc
from selenium_code.section import Section

import gzip

key = Fernet.generate_key() 
print(key)
fernet = Fernet(key) 

class Orchestrator:

    config_list: List

    def __init__(self, configs) -> None:
        self.config_list = []
        self.insert_all_configs(configs)

    def insert_all_configs(self, configs):
        configs = self.sort_configs_sequential_order(configs)
        for config in configs:
            config_object = bc.BaseConfig(config['id'], config['parent_id'], config['name'], config['description'],
                                          config['start_url'], config['path'], config['base_url'], config['pagination'], config['entity_list'],
                                          config['add_base_url'], config['file'], config['scraping_type'])

            self.config_list.append(config_object)

    def extra_config_scrape(self, config_object, start_urls, extra_config):
        if config_object.parent_id == -1:  # first level
            config_object.start_urls.set_start_urls(start_urls)

        # extra config for pagination
        if extra_config is not None:
            for page_config in extra_config:
                if page_config['id'] == config_object.id:
                    if 'max_pages' in list(page_config.keys()) and page_config['max_pages'] is not None:
                        config_object.pagination.set_max_pages(
                            page_config['max_pages'])
                    break

        if config_object.scraping_type == 'scrapy':
            self.scrapy_scraping(config_object)
        elif config_object.scraping_type == 'selenium':
            self.selenium_scraping(config_object)

    def trigger_scraping(self, start_urls, extra_config=None):
        # loop through configs , start_urls is for parent id
        for config_object in self.config_list:
            self.extra_config_scrape(
                config_object=config_object, start_urls=start_urls, extra_config=extra_config)

    def trigger_specific_level_scraping(self, config_id, start_urls, extra_config=None):
        selected_config = None
        for config_object in self.config_list:
            if config_id == config_object.id:
                selected_config = config_object
                break

        if selected_config is not None:
            self.extra_config_scrape(
                config_object=config_object, start_urls=start_urls, extra_config=extra_config)

    def selenium_scraping(self, config_object):
        page_obj = {
            'name' : config_object.name,
            'description': config_object.description,
            'id': config_object.id,
            'start_urls': config_object.start_urls.get_start_urls(),
            'parent_id': str(config_object.parent_id),
            'path': config_object.path.__dict__,
            'base_url': config_object.base_url,
            'pagination': config_object.pagination.__dict__,
            'entities': [entity.__dict__ for entity in config_object.entity_list],
            'add_base_url': config_object.add_base_url,
            'file': config_object.file
        }
        
        Section(page_obj['name'], page_obj['description'], page_obj['id'], page_obj['parent_id'],
                page_obj['path'], page_obj['base_url'], page_obj['start_urls'],
                page_obj['pagination'], page_obj['entities'], page_obj['add_base_url'], page_obj['file'])

    def scrapy_scraping(self, config_object):
        page_obj = {
            'name' : config_object.name,
            'description': config_object.description,
            'id': config_object.id,
            'start_urls': config_object.start_urls.get_start_urls(),
            'parent_id': str(config_object.parent_id),
            'path': config_object.path.__dict__,
            'base_url': config_object.base_url,
            'pagination': config_object.pagination.__dict__,
            'entities': [entity.__dict__ for entity in config_object.entity_list],
            'add_base_url': config_object.add_base_url,
            'file': config_object.file
        }
        
        
        # execute(
        #     [
        #         'scrapy',
        #         'crawl',
        #         'section',
        #         '-a', 'name=' + config_object.name,
        #         '-a', 'description=' + config_object.description,
        #         '-a', 'id=' + str(config_object.id),
        #         '-a', 'parent_id=' + str(config_object.parent_id),
        #         '-a', 'path=' + json.dumps(config_object.path.__dict__),
        #         '-a', 'base_url=' + config_object.base_url,
        #         '-a', 'start_urls=' + json.dumps(config_object.start_urls.get_start_urls()),
        #         '-a', 'pagination=' + json.dumps(config_object.pagination.__dict__),
        #         '-a', 'entities=' + json.dumps([entity.__dict__ for entity in config_object.entity_list]),
        #         '-a', 'add_base_url=' + json.dumps(config_object.add_base_url),
        #         '-a', 'file=' + config_object.file,
        #     ]
        # )

        page_obj = json.dumps(page_obj)
        encMessage = fernet.encrypt(page_obj.encode()) 
       
        new_key = key.decode("utf-8")
        str_message = encMessage.decode("utf-8")
        cmd = f"scrapy crawl section -a message={str_message} -a key={new_key}"
        os.system(cmd)

        

    def sort_configs_sequential_order(self, configs):
        parent_id = -1
        new_config = []
        if len(configs) > 1:
            while len(new_config) < len(configs):
                for config in configs:
                    if config['parent_id'] == parent_id:
                        new_config.append(config)
                        parent_id = config['id']
                        break
            return new_config
        else:
            return configs

    def get_selected_config(self,config_id):
        selected_config = None
        for config_object in self.config_list:
            if config_id == config_object.id:
                selected_config = config_object
                break
        return selected_config
