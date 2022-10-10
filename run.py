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
# FOLDER_2016 = Path.joinpath(DATA_FOLDER, '2016')
# FOLDER_2016.mkdir(parents=True, exist_ok=True)

# LOG_FILE = Path.joinpath(FOLDER_2016, 'crawler.logs')

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
#     start_date = '01.'+str(month).zfill(2)+'.2016'
#     end_date = '01.'+str(month+1).zfill(2)+'.2016'
#     file_name = Path.joinpath(FOLDER_2016, str(month).zfill(2)+'16.json')
#     crawl_and_save_to_file(start_date=start_date, end_date=end_date, file_name=file_name)
# crawl_and_save_to_file(
#     start_date='01.12.2016',
#     end_date='01.01.2017',
#     file_name=Path.joinpath(FOLDER_2016, '1216.json'))


# 2017
# FOLDER_2017 = Path.joinpath(DATA_FOLDER, '2017')
# FOLDER_2017.mkdir(parents=True, exist_ok=True)

# LOG_FILE = Path.joinpath(FOLDER_2017, 'crawler.logs')

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
#     start_date = '01.'+str(month).zfill(2)+'.2017'
#     end_date = '01.'+str(month+1).zfill(2)+'.2017'
#     file_name = Path.joinpath(FOLDER_2017, str(month).zfill(2)+'17.json')
#     crawl_and_save_to_file(start_date=start_date, end_date=end_date, file_name=file_name)
# crawl_and_save_to_file(
#     start_date='01.12.2017',
#     end_date='01.01.2018',
#     file_name=Path.joinpath(FOLDER_2017, '1217.json'))


# 2018
# FOLDER_2018 = Path.joinpath(DATA_FOLDER, '2018')
# FOLDER_2018.mkdir(parents=True, exist_ok=True)

# LOG_FILE = Path.joinpath(FOLDER_2018, 'crawler.logs')

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
#     start_date = '01.'+str(month).zfill(2)+'.2018'
#     end_date = '01.'+str(month+1).zfill(2)+'.2018'
#     file_name = Path.joinpath(FOLDER_2018, str(month).zfill(2)+'18.json')
#     crawl_and_save_to_file(start_date=start_date, end_date=end_date, file_name=file_name)
# crawl_and_save_to_file(
#     start_date='01.12.2018',
#     end_date='01.01.2019',
#     file_name=Path.joinpath(FOLDER_2018, '1218.json'))


# 2019
# FOLDER_2019 = Path.joinpath(DATA_FOLDER, '2019')
# FOLDER_2019.mkdir(parents=True, exist_ok=True)

# LOG_FILE = Path.joinpath(FOLDER_2019, 'crawler.logs')

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
#     start_date = '01.'+str(month).zfill(2)+'.2019'
#     end_date = '01.'+str(month+1).zfill(2)+'.2019'
#     file_name = Path.joinpath(FOLDER_2019, str(month).zfill(2)+'19.json')
#     crawl_and_save_to_file(start_date=start_date, end_date=end_date, file_name=file_name)
# crawl_and_save_to_file(
#     start_date='01.12.2019',
#     end_date='01.01.2020',
#     file_name=Path.joinpath(FOLDER_2019, '1219.json'))


# 2020
# FOLDER_2020 = Path.joinpath(DATA_FOLDER, '2020')
# FOLDER_2020.mkdir(parents=True, exist_ok=True)

# LOG_FILE = Path.joinpath(FOLDER_2020, 'crawler.logs')

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
#     start_date = '01.'+str(month).zfill(2)+'.2020'
#     end_date = '01.'+str(month+1).zfill(2)+'.2020'
#     file_name = Path.joinpath(FOLDER_2020, str(month).zfill(2)+'20.json')
#     crawl_and_save_to_file(start_date=start_date, end_date=end_date, file_name=file_name)
# crawl_and_save_to_file(
#     start_date='01.12.2020',
#     end_date='01.01.2021',
#     file_name=Path.joinpath(FOLDER_2020, '1220.json'))


# 2021
FOLDER_2021 = Path.joinpath(DATA_FOLDER, '2021')
FOLDER_2021.mkdir(parents=True, exist_ok=True)

LOG_FILE = Path.joinpath(FOLDER_2021, 'crawler.logs')

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
    start_date = '01.'+str(month).zfill(2)+'.2021'
    end_date = '01.'+str(month+1).zfill(2)+'.2021'
    file_name = Path.joinpath(FOLDER_2021, str(month).zfill(2)+'21.json')
    crawl_and_save_to_file(start_date=start_date, end_date=end_date, file_name=file_name)
crawl_and_save_to_file(
    start_date='01.12.2021',
    end_date='01.01.2022',
    file_name=Path.joinpath(FOLDER_2021, '1221.json'))
