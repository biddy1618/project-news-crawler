'''
Module for the main script.

Author: Dauren Baitursyn
Date: 11.07.21
'''

import logging
from pathlib import Path

from crawler.crawler import crawl_and_save_to_file

DATA_FOLDER = Path.joinpath(Path.cwd(), 'data')
DATA_FOLDER.mkdir(parents=True, exist_ok=True)

# 2012
FOLDER_2012 = Path.joinpath(DATA_FOLDER, '2012')
FOLDER_2012.mkdir(parents=True, exist_ok=True)

LOG_FILE = Path.joinpath(FOLDER_2012, 'crawler.logs')

logging.basicConfig(
    format='{levelname} {name} {asctime}: {message}',
    level=logging.INFO,
    datefmt='%m/%d/%Y %H:%M:%S',
    style='{',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

MONTHS = list(range(1, 12))

for month in MONTHS:
    start_date = '01.'+str(month).zfill(2)+'.2012'
    end_date = '01.'+str(month+1).zfill(2)+'.2012'
    file_name = Path.joinpath(DATA_FOLDER, str(month).zfill(2)+'12.json')
    crawl_and_save_to_file(start_date=start_date, end_date=end_date, file_name=file_name)
crawl_and_save_to_file(start_date='01.12.2012', end_date='01.01.2013', file_name='./data/1212.json')
