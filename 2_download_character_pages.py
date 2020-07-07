import pandas as pd
import os
import requests
import random
import json
import argparse
from time import sleep
from lib import utils

from IPython.display import display, clear_output

# Commandline argument parser
parser = argparse.ArgumentParser(description='Receive crawling options from commandline.')
parser.add_argument('-s', '--start_point', type=int, help='Starting index of the list of characters to crawl')
parser.add_argument('-e', '--end_point', type=int, help='Ending index of the list of characters to crawl')

args = parser.parse_args()

# Prepare craw list
char_list = pd.read_csv('data/raw/character_list.csv')

save_interval = 5

if args.start_point is not None:
    start_point = args.start_point
else:
    start_point = 0

if args.end_point is not None:
    end_point = args.end_point
else:
    end_point = -1

if os.path.exists('progress') == False:
    os.makedirs('progress')

# try:
#     with open('progress/characters_progress.json', 'r') as obj:
#         last_progress = json.load(obj)
#         print('Last saved character index: {}'.format(last_progress['char_index']))
#         start_point = last_progress['char_index']
        
# except FileNotFoundError as error:
#     print('Progress file not found. Start from beginning.')
    
# except json.JSONDecodeError as error:
#     print('No progress found. Start from beginning')

crawl_list = char_list.url[start_point:end_point]

for counter, url in enumerate(crawl_list, start=1):
    
    words = url.split('/')
    char = words[len(words) - 1]
    
    clear_output(wait=True)
    print('Downloading page {} - {}'.format(start_point + counter, char))
    
    page_res = requests.get(url)
    page_res.raise_for_status()
    
    utils.save_html(page_res, 'character_pages/', char + '.html')
    
    char_progress = {'char_index': start_point + counter - 1}
    
    if counter % save_interval == 0:
        with open('progress/characters_progress.json', 'w') as obj:
            json.dump(char_progress, obj)
    
    sleep(random.randint(2, 10))

