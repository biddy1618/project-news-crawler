from crawler.crawler import Crawler
from helper import Helper
from db import db, models

import logging
import os

from dotenv import load_dotenv
load_dotenv()

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
s = db.Session()

def crawler_test(dateFirst = '01.01.2012', dateLast = '01.01.2013'):
    dates = Helper.generate_dates(dateFirst, dateLast)

    for d in dates:
        res = set()
        
        r_link_date = crawler.get_url(
            crawler.URL_ARCHIVE,
            {'date': d}
        )
    
        links = crawler.get_links(r_link_date)
        
        for l in links:
            if l in res:
                print(f'Duplicate article URL: {l}')
                continue
            r_page = crawler.get_url(l)
            res.add(l)
            crawler.extract_article(r_page)
        
def crawler_test_article(url):
    r_page = crawler.get_url(url)
    article = crawler.extract_article(r_page)
    return article

# models.Base.metadata.drop_all(db.engine)
models.Base.metadata.create_all(db.engine)
s = db.Session()

# db.crawl_and_save_to_db("01.01.2012", end_date="01.01.2013", s=s)
# db.crawl_and_save_to_db("16.05.2012", end_date="01.01.2014", s=s)
# db.crawl_and_save_to_db("30.06.2012", end_date="01.01.2014", s=s)
# db.crawl_and_save_to_db("09.07.2012", end_date="01.01.2014", s=s)
# db.crawl_and_save_to_db("04.12.2012", end_date="01.01.2014", s=s)
db.crawl_and_save_to_db("11.01.2013", end_date="01.01.2014", s=s)

# print(crawler_test_article('https://www.inform.kz/ru/v-zhanaozene-prodolzhaetsya-rabota-po-blagoustroystvu-goroda_a2430452'))