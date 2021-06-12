import enum
from typing import List

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import selenium
from selenium.webdriver.common.keys import Keys


class Driver:
    driver: any;
    
    def __init__(self) -> None:
        PROXY = ''
        # rotating proxies
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY,
            "proxyType": "MANUAL",
        }
        options = webdriver.ChromeOptions()

        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Chrome(executable_path='D:/Office/chromedriver.exe', options=options)
        
        self.driver.set_window_size(1024, 600)
        self.driver.maximize_window()

    def get_driver(self,url):
        self.driver.get(url);
        time.sleep(3)
        self.scroll(4)
        return self.driver

    def scroll(self, timeout):
        scroll_pause_time = timeout

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # If heights are the same it will exit the function
                break
            last_height = new_height


    def __del__(self):  
        self.driver.quit();

