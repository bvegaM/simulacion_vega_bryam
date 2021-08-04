import coloredlogs
import requests
import bs4
import numpy as np
import time
import logging
logging.basicConfig(level=logging.INFO)

import warnings
warnings.filterwarnings("ignore")

from common import config

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from requests.exceptions import HTTPError
from socket import gaierror
from urllib3.exceptions import MaxRetryError,NewConnectionError



CHROMEDRIVERPATH = '../driver/chromedriver'
WINDOWS_SIZE     = '1920,2048'
chrome_options   = Options()
chrome_options.add_argument('--window-size=%s'%WINDOWS_SIZE)

logger = logging.getLogger(__name__)
coloredlogs.install()

class NewSite:

    def visit(self):
        try:
            response = requests.get(self._url)
            response.encoding='utf-8'
            response.raise_for_status()
            self._html = bs4.BeautifulSoup(response.text,'html.parser')
        except Exception:
           logger.warning('Connection refused',exc_info=False)

    def visit_search(self):
        self._driver = webdriver.Chrome(executable_path=CHROMEDRIVERPATH,chrome_options=chrome_options)
        self._driver.get(self._url)

        search = ''
        if self._config['scroll_url']:
            search = self._driver.find_element(By.CLASS_NAME,self._config['scroll_url']).click()
            search = self._driver.find_element_by_name(self._queries['article_search'])
        else:
            search = self._driver.find_element_by_name(self._queries['article_search'])

        search.send_keys(self._queries['searcher'])
        search.submit()
    
    def flatten(self,list_of_lists):
        if len(list_of_lists) == 0:
            return list_of_lists
        if isinstance(list_of_lists[0], list):
            return self.flatten(list_of_lists[0]) + self.flatten(list_of_lists[1:])
        return list_of_lists[:1] + self.flatten(list_of_lists[1:])
    
    def get_url(self,list_results):
        return[item.find_element(By.CSS_SELECTOR,self._queries['article_link']).get_attribute('href') for item in list_results]
    
    def get_links(self):
        i=1
        results=[]
        while i<=self._queries['max_find']:
            list_result = self._driver.find_elements(By.CLASS_NAME,self._queries['article_struct'])
            if len(list_result)>0:
                results.append(self.get_url(list_result))
                i+=1
                self._driver.get(self._next_page.format(i))
                time.sleep(self._queries['sleep'])
            else:
                break
        return self.flatten(results)

    def __init__(self,site_uid,url):
        self._config     = config()['sites'][site_uid]
        self._queries    = self._config['queries']
        self._url        = url
        self._next_page  = config()['sites'][site_uid]['next_page']
        self._driver     = None
        self._html       = None

class ArticlePage(NewSite):

    def __init__(self,news_site_uid,url):
        super().__init__(news_site_uid,url)
        try:
            self.visit()
        except Exception:
           logger.warning('Connection refused',exc_info=False)

    @property
    def get_abstract(self):
        try:
            abstract = self._html.select(self._queries['article_abstract'])
            return abstract[0].text
        except (IndexError, AttributeError):
            logger.warning('Problem with the article ',exc_info=False)
            return ''
        

