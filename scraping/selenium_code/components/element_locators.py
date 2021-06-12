from enum import Enum

class ElementLocators(Enum):
    XpathSelector = 'xpath'
    ClassSelector = 'css'

class XpathSelector():
    path: str;

    def __init__(self, path, dtype=None) -> None:
        self.path = path
        self.dtype = dtype

    def get(self, driver):
        try:
            element = driver.find_element_by_xpath(self.path)
            if self.dtype == 'text':
                return self.get_text(element) 
            elif self.dtype == 'url':
                return self.get_url(element)
            else: 
                return element
        except:
            return ''

    def get_all(self, driver):
        return driver.find_elements_by_xpath(self.path)

    def get_text(self,element):
        return element.text

    def get_url(self,element):
        return element.get_attribute('href')

class ClassSelector():
    path: str;

    def __init__(self, path, dtype=None) -> None:
        self.path = path
        self.dtype = dtype

    def get(self, driver):
        element = driver.find_element_by_class_name(self.path)
        if self.dtype == 'text':
            return self.get_text(element) 
        elif self.dtype == 'url':
            return self.get_url(element)
        else:
            return element


    def get_all(self, driver):
        return driver.find_elements_by_class_name(self.path)

    def get_text(element):
            return element.text

    def get_url(element):
        return element.get_attribute('href')


class Switcher():
    selected_class: any;

    def __init__(self,element_locator) -> None:
        self.selected_class = XpathSelector if element_locator == ElementLocators['XpathSelector'].value else ClassSelector

    def get_class(self):
        return self.selected_class
