'''
Module for crawler main functions. It returns the list of articles given the date range.
The main function `crawl_and_save_to_file` uses locally defined functions:
`_get_session`
`_close_session`
`_get_url`
`_crawl_for_date`

Author: Dauren Baitursyn
Date: 11.07.21
'''

import requests
import logging
import time
import json

import urllib.parse as urlparse

from typing import Dict

import helper
from crawler.links import get_links, get_pages
from crawler.article import get_article

logger = logging.getLogger(__name__)

URL_ARCHIVE = 'https://www.inform.kz/ru/archive'
TIMEOUT = 5


def _get_session() -> requests.Session:
    '''
    Gets instance of session from requests package

    Returns:
        requests.Session: Session object.
    '''
    return requests.Session()


def _close_session(session: requests.Session):
    '''
    Close the session associated with the crawler.

    Args:
        session (requests.Session): Session to close
    '''
    session.close()


def _get_url(session: requests.Session, url: str, params: Dict[str, str] = None) -> requests.Response:
    '''
    Fetch the URL provided and return response object.

    Args:
        session (requests.Session): Session object.
        url (str): URL provided.
        params (Dict[str, str]): Query parameters in dictinary format.

    Returns:
        requests.Response: HTML page fetched with response code or None in case of exception.
    '''
    if params:
        url_parsed = urlparse.urlparse(url)
        url_str = url_parsed._replace(
            query=urlparse.urlencode(dict(urlparse.parse_qsl(url_parsed.query), **params))).geturl()
    else:
        url_str = url
    for i in range(10):
        try:
            r = session.get(url, params=params, timeout=TIMEOUT)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            if i == 9:
                logger.error(
                    helper._message(f'Failed to get the URL {url_str}', e))
                return None
            logger.warning(
                helper._message(f'Failed to get the URL {url_str}, retrying in 0.1 seconds.', e))
            time.sleep(0.1)
        else:
            logger.info(helper._message(f'Success retrieving URL {url_str}'))
            break
    return r


def _crawl_for_date(session: requests.Session, date: str, log_every: int = None) -> dict:
    '''
    Retrieve articles for the given date.

    Args:
        session (requests.Session): Session object.
        date (str): Date in format "dd.mm.yyyy".
        log_every (int, optional): Log message every nth retrieved record.
            Defaults to None in which case doesn't log.

    Returns:
        list: List of retrieved articles.
    '''
    articles = []
    r_main = _get_url(session, URL_ARCHIVE, {'date': date})

    r_allpages = get_pages(r_main)
    r_allpages = [r_main] + [_get_url(session, page) for page in r_allpages]
    url_links = get_links(r_allpages)
    logger.info(helper._message(f'Retrieving {len(url_links)} articles for the date: {date}'))
    for i, link in enumerate(url_links):
        page = _get_url(session, link)
        article = get_article(page)
        if article is None:
            continue
        articles.append(article)
        if log_every and i+1 % log_every == 0:
            logger.info(helper._message(f'Retrieved {log_every} articles.'))

    logger.info(helper._message('Retrieved all articles.'))

    return articles


def crawl_and_save_to_file(start_date: str, file_name: str, end_date: str = None) -> None:
    '''
    Crawl data for the given date(s) and save it to file system.

    Args:
        start_date (str): Start date to crawl.
        file_name (str): File name to save the crawled files.
        end_date (str, optional): End date to crawl. Defaults to None.
    '''
    dates = helper.generate_dates(start_date, end_date)
    session = _get_session()
    final = []
    for d in dates:
        articles = _crawl_for_date(session=session, date=d)
        final.extend(articles)

    _close_session(session)
    with open(file_name, 'w', encoding='utf8') as json_file:
        json.dump(final, json_file, ensure_ascii=False)
