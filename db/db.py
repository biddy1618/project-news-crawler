'''
Module for database interaction methods.

Author: Dauren Baitursyn
Date: 11.07.21
'''

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from dotenv import load_dotenv

import os
import logging
from pathlib import Path

from db import models
from crawler.crawler import Crawler
import helper

env_path = Path(__file__).parents[1].absolute() / '.env'
print(env_path)
load_dotenv(env_path)


PG_USER = os.getenv('PG_USER', 'dauren')
PG_PASSWORD = os.getenv('PG_PASSWORD', 'changeme')
PG_URL = os.getenv('PG_URL', 'localhost:5432')
PG_DATABSE = os.getenv('PG_DATABASE', 'news')

PG_URI = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_URL}/{PG_DATABSE}'

if not database_exists(PG_URI):
    create_database(PG_URI)

engine = create_engine(PG_URI)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(engine)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def crawl_and_save_to_db(start_date: str, s: sqlalchemy.orm.Session, end_date: str = None) -> None:
    '''
    Crawl data for the given date(s) and save it to DB.

    Args:
        start_date (str): Start date to crawl.
        s (sqlalchemy.orm.Session): Session object through which writing to DB is performed.
        end_date (str, optional): End date to crawl. Defaults to None.
    '''
    crawler = Crawler()
    dates = helper.generate_dates(start_date, end_date)
    for d in dates:
        data = crawler.crawl_for_date(date=d)

        logger.info(helper._message(f'Saving {len(data["articles"])} articles.'))
        a_len = len(data['articles'])
        for a in data['articles']:
            if models.insert_article(a, s) is None:
                a_len -= 1
            try:
                s.commit()
            except sqlalchemy.exc.DBAPIError as e:
                logger.error(helper._message(f'Error at insertion of the following article: {a["url"]}', e))
                s.rollback()
                a_len -= 1
        logger.info(helper._message(f'Successfully saved {a_len} articles.'))

        # logger.info(helper._message(f'Saving {len(data["links"])} links.'))
        # l_len = len(data["links"])
        # for l in data['links']:
        #     if models.insert_link(l, s) is None: l_len -= 1
        #     try:
        #         s.commit()
        #     except sqlalchemy.exc.DBAPIError as e:
        #         logger.error(helper._message(f'Error at insertion of the following link: {l}', e))
        #         s.rollback()
        #         l_len -= 1
        # logger.info(helper._message(f'Successfully saved {l_len} links.'))

        logger.info(helper._message(f'Saving {len(data["tags"])} tags.'))
        t_len = len(data["tags"])
        for t in data['tags']:
            if models.insert_tag(t, s) is None:
                t_len -= 1
            try:
                s.commit()
            except sqlalchemy.exc.DBAPIError as e:
                logger.error(helper._message(f'Error at insertion of the following tag: {t}', e))
                s.rollback()
                t_len -= 1
        logger.info(helper._message(f'Successfully saved {t_len} tags.'))

    crawler.close()
