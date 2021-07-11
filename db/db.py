import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv

import os
import logging

from db import models
from helper import Helper
from crawler.crawler import Crawler

load_dotenv()

engine = create_engine(os.getenv('DB_URI_DEV'))
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(engine)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def crawl_and_save_to_db(start_date: str, s: sqlalchemy.orm.Session, end_date: str = None) -> None:
    """
    Crawl data for the given date(s) and save it to DB.

    Args:
        start_date (str): Start date to crawl.
        s (sqlalchemy.orm.Session): Session object through which writing to DB is performed.
        end_date (str, optional): End date to crawl. Defaults to None.
    """
    crawler = Crawler()
    dates = Helper.generate_dates(start_date, end_date)
    for d in dates:
        data = crawler.crawl_for_date(date=d)
        print(data)
        
        logger.info(Helper._message(f'Saving {len(data["articles"])} articles.'))
        a_len = len(data['articles'])
        for a in data['articles']:
            if models.insert_article(a, s) is None: a_len -= 1
            try:
                s.commit()
            except sqlalchemy.exc.DBAPIError as e:
                logger.error(Helper._message(f'Error at insertion of the following article: {a["url"]}', e))
                s.rollback()
                a_len -= 1
        logger.info(Helper._message(f'Successfully saved {a_len} articles.'))
        
                
        # logger.info(Helper._message(f'Saving {len(data["links"])} links.'))
        # l_len = len(data["links"])
        # for l in data['links']:
        #     if models.insert_link(l, s) is None: l_len -= 1
        #     try:
        #         s.commit()
        #     except sqlalchemy.exc.DBAPIError as e:
        #         logger.error(Helper._message(f'Error at insertion of the following link: {l}', e))
        #         s.rollback()
        #         l_len -= 1
        # logger.info(Helper._message(f'Successfully saved {l_len} links.'))
        
        logger.info(Helper._message(f'Saving {len(data["tags"])} tags.'))
        t_len = len(data["tags"])
        for t in data['tags']:
            if models.insert_tag(t, s) is None: t_len -= 1
            try:
                s.commit()
            except sqlalchemy.exc.DBAPIError as e:
                logger.error(Helper._message(f'Error at insertion of the following tag: {t}', e))
                s.rollback()
                t_len -= 1
        logger.info(Helper._message(f'Successfully saved {t_len} tags.'))
            
    crawler.close()
