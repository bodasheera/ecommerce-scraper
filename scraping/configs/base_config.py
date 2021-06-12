from typing import List
import pandas as pd


class Path:
    type: str
    value: str

    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value


class Pagination(Path):

    route: str;

    def __init__(self, type = None , value = None , route=None, max_pages = None) -> None:
        super().__init__(type, value)
        self.route = route
        self.max_pages = max_pages

    def set_max_pages(self, max_pages):
        self.max_pages = max_pages


class StartUrls():

    def __init__(self, urls=[] , file = None , column = None) -> None:
        self.urls = [] if urls == None else urls
        self.file = file
        self.column = column

    def get_start_urls(self):
        if len(self.urls) > 0:
            return self.urls
        else:
            data = pd.read_csv('scraping/output/' + self.file + '.csv')[self.column].to_list()
            if len(data) > 5:
                return data[0:5]
            else:
                return data

    def set_start_urls(self,url_list):
        self.urls = url_list


class Entity:
    name: str
    value: str
    attribute: str
    type: str
    
    def __init__(self, name, value, type, attribute=None) -> None:
        self.name = name
        self.value = value
        self.type = type
        self.attribute = attribute


class BaseConfig:
    id: int
    parent_id: int
    name: str
    description: str
    path: object
    base_url: str
    start_urls: List
    pagination: object
    entity_list: List
    add_base_url: List
    file: str
    scraping_type: str

    def __init__(self, id, parent_id, name, description,start_url, path, base_url, pagination, entity_list, add_base_url, file, scraping_type) -> None:
        self.id = id
        self.parent_id = parent_id
        self.name = name
        self.description = description
        self.path = Path(path['type'], path['value'])
        self.base_url = base_url
        self.start_urls = StartUrls(None, start_url['file'], start_url['column'])
        self.pagination = Pagination(pagination['type'], pagination['value'])
        self.entity_list = self.get_entity_list(entity_list)
        self.add_base_url = add_base_url
        self.file = file
        self.scraping_type = scraping_type


    def get_entity_list(self, entity_list) -> List:
        ent_list = []
        for entity in entity_list:
            if 'attribute' in entity:
                ent_list.append(
                    Entity(entity['name'], entity['value'], entity['type'], entity['attribute']))
            else:
                ent_list.append(
                    Entity(entity['name'], entity['value'], entity['type']))
        return ent_list

    def get_start_url(self, input_str):
        file, param = input_str.replace(" ", "").split('|')
        return pd.read_csv('scraping/output/' + file + '.csv')[param].to_list()

