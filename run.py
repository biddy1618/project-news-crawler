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
# FOLDER_2012 = Path.joinpath(DATA_FOLDER, '2012')
# FOLDER_2012.mkdir(parents=True, exist_ok=True)

# LOG_FILE = Path.joinpath(FOLDER_2012, 'crawler.logs')

# logging.basicConfig(
#     format='{levelname} {name} {asctime}: {message}',
#     level=logging.INFO,
#     datefmt='%m/%d/%Y %H:%M:%S',
#     style='{',
#     handlers=[
#         logging.FileHandler(LOG_FILE),
#         logging.StreamHandler()
#     ]
# )

# MONTHS = list(range(1, 12))

# for month in MONTHS:
#     start_date = '01.'+str(month).zfill(2)+'.2012'
#     end_date = '01.'+str(month+1).zfill(2)+'.2012'
#     file_name = Path.joinpath(FOLDER_2012, str(month).zfill(2)+'12.json')
#     crawl_and_save_to_file(start_date=start_date, end_date=end_date, file_name=file_name)
# crawl_and_save_to_file(
#     start_date='01.12.2012',
#     end_date='01.01.2013',
#     file_name=Path.joinpath(FOLDER_2012, '1212.json'))


# 2013
# FOLDER_2013 = Path.joinpath(DATA_FOLDER, '2013')
# FOLDER_2013.mkdir(parents=True, exist_ok=True)

# LOG_FILE = Path.joinpath(FOLDER_2013, 'crawler.logs')

# logging.basicConfig(
#     format='{levelname} {name} {asctime}: {message}',
#     level=logging.INFO,
#     datefmt='%m/%d/%Y %H:%M:%S',
#     style='{',
#     handlers=[
#         logging.FileHandler(LOG_FILE),
#         logging.StreamHandler()
#     ]
# )

# MONTHS = list(range(1, 12))

# for month in MONTHS:
#     start_date = '01.'+str(month).zfill(2)+'.2013'
#     end_date = '01.'+str(month+1).zfill(2)+'.2013'
#     file_name = Path.joinpath(FOLDER_2013, str(month).zfill(2)+'13.json')
#     crawl_and_save_to_file(start_date=start_date, end_date=end_date, file_name=file_name)
# crawl_and_save_to_file(
#     start_date='01.12.2013',
#     end_date='01.01.2014',
#     file_name=Path.joinpath(FOLDER_2013, '1213.json'))


# 2014
# FOLDER_2014 = Path.joinpath(DATA_FOLDER, '2014')
# FOLDER_2014.mkdir(parents=True, exist_ok=True)

# LOG_FILE = Path.joinpath(FOLDER_2014, 'crawler.logs')

# logging.basicConfig(
#     format='{levelname} {name} {asctime}: {message}',
#     level=logging.INFO,
#     datefmt='%m/%d/%Y %H:%M:%S',
#     style='{',
#     handlers=[
#         logging.FileHandler(LOG_FILE),
#         logging.StreamHandler()
#     ]
# )

# MONTHS = list(range(1, 12))

# for month in MONTHS:
#     start_date = '01.'+str(month).zfill(2)+'.2014'
#     end_date = '01.'+str(month+1).zfill(2)+'.2014'
#     file_name = Path.joinpath(FOLDER_2014, str(month).zfill(2)+'14.json')
#     crawl_and_save_to_file(start_date=start_date, end_date=end_date, file_name=file_name)
# crawl_and_save_to_file(
#     start_date='01.12.2014',
#     end_date='01.01.2015',
#     file_name=Path.joinpath(FOLDER_2014, '1214.json'))


# 2015
# FOLDER_2015 = Path.joinpath(DATA_FOLDER, '2015')
# FOLDER_2015.mkdir(parents=True, exist_ok=True)

# LOG_FILE = Path.joinpath(FOLDER_2015, 'crawler.logs')

# logging.basicConfig(
#     format='{levelname} {name} {asctime}: {message}',
#     level=logging.INFO,
#     datefmt='%m/%d/%Y %H:%M:%S',
#     style='{',
#     handlers=[
#         logging.FileHandler(LOG_FILE),
#         logging.StreamHandler()
#     ]
# )

# MONTHS = list(range(1, 12))

# for month in MONTHS:
#     start_date = '01.'+str(month).zfill(2)+'.2015'
#     end_date = '01.'+str(month+1).zfill(2)+'.2015'
#     file_name = Path.joinpath(FOLDER_2015, str(month).zfill(2)+'15.json')
#     crawl_and_save_to_file(start_date=start_date, end_date=end_date, file_name=file_name)
# crawl_and_save_to_file(
#     start_date='01.12.2015',
#     end_date='01.01.2016',
#     file_name=Path.joinpath(FOLDER_2015, '1215.json'))


# 2016
FOLDER_2016 = Path.joinpath(DATA_FOLDER, '2016')
FOLDER_2016.mkdir(parents=True, exist_ok=True)

LOG_FILE = Path.joinpath(FOLDER_2016, 'crawler.logs')

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
    start_date = '01.'+str(month).zfill(2)+'.2016'
    end_date = '01.'+str(month+1).zfill(2)+'.2016'
    file_name = Path.joinpath(FOLDER_2016, str(month).zfill(2)+'16.json')
    crawl_and_save_to_file(start_date=start_date, end_date=end_date, file_name=file_name)
crawl_and_save_to_file(
    start_date='01.12.2016',
    end_date='01.01.2017',
    file_name=Path.joinpath(FOLDER_2016, '1216.json'))
