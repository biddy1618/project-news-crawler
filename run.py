'''
Module for the main script.

Author: Dauren Baitursyn
Date: 11.07.21
'''

from crawler.crawler import Crawler, crawl_and_save_to_file
import helper
# from db import db, models

import logging
import os

from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).parents[0].absolute() / '.env'
print(env_path)
load_dotenv(env_path)

LOG_FILE = os.getenv('LOG_FILE', 'crawler.logs')

logging.basicConfig(
    format='{levelname} {name} {asctime}: {message}',
    level=logging.INFO,
    datefmt='%m/%d/%Y %H:%M:%S',
    style='{',
    handlers=[
        logging.FileHandler(os.getenv('LOG_FILE')),
        logging.StreamHandler()
    ]
)

crawler = Crawler()
# s = db.Session()


def crawler_test(dateFirst='01.01.2012', dateLast='01.01.2013'):
    dates = helper.generate_dates(dateFirst, dateLast)

    for d in dates:
        res = set()

        r_link_date = crawler.get_url(
            crawler.URL_ARCHIVE,
            {'date': d}
        )

        links = crawler.get_links(r_link_date)

        for link in links:
            if link in res:
                print(f'Duplicate article URL: {link}')
                continue
            r_page = crawler.get_url(link)
            res.add(link)
            crawler.extract_article(r_page)


def crawler_test_article(url):
    r_page = crawler.get_url(url)
    article = crawler.extract_article(r_page)
    return article


# models.Base.metadata.drop_all(db.engine)
# models.Base.metadata.create_all(db.engine)
# s = db.Session()

# db.crawl_and_save_to_db("01.01.2012", end_date="15.10.2012", s=s)
# db.crawl_and_save_to_db("15.10.2012", end_date="01.01.2013", s=s)
# db.crawl_and_save_to_db("01.01.2013", end_date="03.09.2014", s=s)
# db.crawl_and_save_to_db("03.09.2014", end_date="01.01.2015", s=s)
# db.crawl_and_save_to_db("09.07.2012", end_date="01.01.2014", s=s)
# db.crawl_and_save_to_db("04.12.2012", end_date="01.01.2014", s=s)
# db.crawl_and_save_to_db("11.01.2013", end_date="01.01.2014", s=s)


crawl_and_save_to_file('01.01.2012', end_date='05.01.2012')
# print(crawler_test_article('https://www.inform.kz/ru/vengry-protestuyut-protiv-novoy-konstitucii-strany_a2430500'))
