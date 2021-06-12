from enum import Enum
from typing import List 

class ElementLocators(Enum):
    XpathSelector = 'xpath'
    ClassSelector = 'css'


class XpathSelector():
    def __init__(self, path) -> None:
        self.path = path

    def get(self, response):
        return response.xpath(self.path).get()

    def get_all(self, response):
        return response.xpath(self.path).getall()

    def get_html(self, response):
        return response.xpath(self.path)


class ClassSelector():

    def __init__(self, path) -> None:
        self.path = path

    def get(self, response):
        return response.css(self.path).get()

    def get_all(self, response):
        return response.css(self.path).getall()

    def get_html(self, response):
        return response.css(self.path)


class Switcher():

    def __init__(self,element_locator) -> None:
        self.selected_class = XpathSelector if element_locator == ElementLocators['XpathSelector'].value else ClassSelector

    def get_class(self):
        return self.selected_class
