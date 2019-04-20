import pandas as pd
import bs4
import requests
from urllib.parse import urljoin
from time import sleep
from lib import utils

# Get character URLs from all pages
# Initiate
base_url = 'https://wiki.lspace.org/'
first_page_url = 'https://wiki.lspace.org/mediawiki/Category:Discworld_characters'

page_res = requests.get(first_page_url)
page_res.raise_for_status()
page_soup = bs4.BeautifulSoup(page_res.content, features='lxml')

char_urls = utils.get_char_urls(page_soup)

# Go through next pages
next_page_soup = page_soup
next_page_urls = []

while utils.next_page_exists(next_page_soup):
    
    pagenum = len(next_page_urls) + 1
    
    print('Checking page {}'.format(pagenum), end = '\r')
    page_navs = list(set(next_page_soup.select('div #mw-pages > a')))

    for elm in page_navs:
        if elm.getText() == 'next page':
            next_path = elm.get('href')
            next_url = urljoin(base_url, next_path)
            break
        else:
            next
    
    next_page_urls.append(next_url)
    next_page_res = requests.get(next_url)
    next_page_res.raise_for_status()
    next_page_soup = bs4.BeautifulSoup(next_page_res.content, features='lxml')
    
    new_char_urls = utils.get_char_urls(next_page_soup)
    
    char_urls['char_name'] += new_char_urls['char_name']
    char_urls['url'] += new_char_urls['url']
    
    sleep(2)

char_urls_df = pd.DataFrame(char_urls)
char_urls_df.to_csv('data/raw/character_list.csv', index=False)
