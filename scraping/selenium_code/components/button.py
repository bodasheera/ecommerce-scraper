import time
from selenium.webdriver.common.action_chains import ActionChains

def get_button(base):

    class Button(base):
        
        def __init__(self, path, disabled_property=None) -> None:
            super().__init__(path)
            self.disabled_property = disabled_property

        def click(self,driver):
            button_element = super().get(driver)
            actions = ActionChains(driver)
            actions.move_to_element(button_element).perform() 
            time.sleep(5)        

            # next button is disabled in the last page   
            if self.disabled_property is not None:
                attr = True if button_element.get_attribute(self.disabled_property) is None else False  
                button_element.click()   
                return attr

            # next button is not present in last page
            try:
                button_element.click()   
                return True
            except:
                return False


    return Button