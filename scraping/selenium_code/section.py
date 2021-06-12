from typing import List
from .components import element_locators as el
from .components import entity as e
from .components import driver as d
from .components import button as b
import pandas as pd
import time 


class Section:
    name = 'section'
    section_name : str;        
    description: str;
    base_path : any;
    id: int;
    parent_id: int;
    base_url: str;
    # start_urls = []
    entityList: List;
    pagination: any; 
    final_data: List;
    add_base_url: List;
    file: str;
    driver: any;

    def __init__(self, name, description, id, parent_id , path , base_url, start_urls, pagination, entities, add_base_url, file) -> None:
        self.section_name = name
        self.description = description
        self.add_base_url = add_base_url
        self.set_base_path(path)
        self.id = id
        self.parent_id = parent_id
        self.start_urls = start_urls
        self.base_url = base_url
        self.set_pagination(pagination)
        self.final_data = []
        self.driver = d.Driver()
        self.entityList = []
        self.set_entities(entities)
        self.file = file 
        self.start_scraping()

    def set_base_path(self,base_path):
        element_locator_id = base_path['type']
        path = base_path['value']
        self.base_path = (el.Switcher(element_locator_id).get_class())(path)

    def set_pagination(self,pagination):
        if pagination is not None: 
            element_locator_id = pagination['type']
            path = pagination['value']
            # element_locator_id , path = pagination[:2]
            disabled_property = pagination['disabled'] if 'disabled' in pagination.keys() else None
            s = el.Switcher(element_locator_id).get_class()
            self.pagination = (b.get_button(s))(path,disabled_property)
        else:
            self.pagination = None 


    def set_entities(self,entities):
        for entity in entities: 
            # name, path, data_type , element_locator_id = entity
            name = entity['name']
            path = entity['value']
            data_type = entity['attribute']
            element_locator_id = entity['type']
            s = el.Switcher(element_locator_id)
            entity_object = (e.get_entity(s.get_class()))(name, path, data_type)
            self.entityList.append(entity_object)
        
    def start_scraping(self):
        for url in self.start_urls:
            paginate = True
            driver_value = None 
            while(paginate):
                result = {}
                result['start_url'] = url
                if driver_value is None:
                    driver_value = self.driver.get_driver(url)
                else:
                    self.driver.scroll(5)
                for base_dataset in self.base_path.get_all(driver_value):
                    for entity in self.entityList:
                        if entity.get(base_dataset) is not None and entity.name in self.add_base_url:
                            value = self.base_url + entity.get(base_dataset)
                        else:
                            value = entity.get(base_dataset)
                        result[entity.name] = value 
                    self.final_data.append(result)
                    result = {}
                    result['start_url'] = url
                try:
                    if self.pagination is not None:
                        paginate = self.pagination.click(driver_value)
                        time.sleep(3)
                    else:
                        paginate = False
                except:
                    paginate = False
        self.save_data()

    def save_data(self):
        df = pd.DataFrame.from_records(self.final_data)
        df.to_csv('scraping/output/' + self.file + '.csv', index= False, encoding='utf-8-sig')