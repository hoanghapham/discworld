import pandas as pd
import bs4
import requests
import os
from urllib.parse import urljoin

class NoElementError(Exception):
    
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return(repr(self.value))

def get_char_urls(page_soup):
    
    base_url = 'https://wiki.lspace.org/'
    char_elms = page_soup.select('.mw-category-group a')
    
    if len(char_elms) == 0:
        raise NoElementError('No character element found.')
        
    else:
        char_urls = {
            'char_name': []
            , 'url': []
        }

        for counter, elm in enumerate(char_elms):
            char_urls['char_name'].append(elm.getText())
            url = urljoin(base_url, elm.get('href'))
            char_urls['url'].append(url)

        return char_urls

def next_page_exists(page_soup):
    page_navs = list(set(page_soup.select('div #mw-pages > a')))
    check = any(
        page_navs[x].getText() == 'next page' for x in range(len(page_navs)))
    return check

def save_html(res, dir_path, file_name):
    
    if os.path.exists(dir_path) == False:
        os.makedirs(dir_path)
    
    with open(os.path.join(dir_path, file_name), 'wb') as obj:
        for chunk in res.iter_content(100000):
            obj.write(chunk)
    
