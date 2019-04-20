import pandas as pd
import os
import requests
from time import sleep
from lib import utils
import json
from IPython.display import display, clear_output

if os.path.exists('progress') == False:
    os.makedirs('progress')

char_list = pd.read_csv('data/raw/character_list.csv')

save_interval = 5
start_point = 0

try:
    with open('progress/characters_progress.json', 'r') as obj:
        last_progress = json.load(obj)
        print('Last saved character index: {}'.format(last_progress['char_index']))
        start_point = last_progress['char_index']
        
except FileNotFoundError as error:
    print('Progress file not found. Start from beginning.')
    
except json.JSONDecodeError as error:
    print('No progress found. Start from beginning')

crawl_list = char_list.url[start_point:-1]

for counter, url in enumerate(crawl_list, start=1):
    
    words = url.split('/')
    char = words[len(words) - 1]
    
    clear_output(wait=True)
    print('Downloading page {} - {}'.format(start_point + counter, char))
    
    page_res = requests.get(url)
    page_res.raise_for_status()
    
    utils.save_html(page_res, 'character_pages/', char + '.html')
    
    char_progress = {'char_index': counter - 1}
    
    if counter % save_interval == 0:
        with open('progress/characters_progress.json', 'w') as obj:
            json.dump(char_progress, obj)
    
    sleep(2)
