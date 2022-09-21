'''
Module for crawling article given the Response object of the article link.
The main function `get_article` uses locally defined functions:
`_get_author`
`_get_title`
`_get_date`
`_get_reference_links`
`_get_body`
`_get_tags`


Author: Dauren Baitursyn
Date: 11.07.21
'''

import requests
import logging
import re

import urllib.parse as urlparse

from bs4 import BeautifulSoup as bs
from typing import List, Optional, Dict

import helper

URL_MAIN = 'https://www.inform.kz'
logger = logging.getLogger(__name__)


def _get_title(soup: bs, url: str) -> str:
    '''
    Get the title of the article from BS object.

    Args:
        soup (bs): BS object.
        url (str): URL of the article (for reporting exceptions).

    Returns:
        str: Title of the article or None in case of exception.
    '''
    try:
        title = soup.find('div', class_='title_article_bl')
        title = re.sub(r'\s+', ' ', title.get_text().strip())
    except AttributeError as e:
        logger.error(helper._message(f'Failed to fetch title at URL {url}', e))
        # raise SystemExit(e)
        return None
    return title


def _get_date(soup: bs, url: str) -> str:
    '''
    Get the date of the article from BS object.

    Args:
        soup (bs): BS object.
        url (str): URL of the article (for reporting exceptions).

    Returns:
        str: Date of the article or None in case of exception.
    '''
    try:
        date = soup.find('div', class_='time_article_bl')
        date = re.sub(r'\s+', ' ', date.get_text().strip())
    except AttributeError as e:
        logger.error(helper._message(f'Failed to fetch date at URL {url}', e))
        # raise SystemExit(e)
        return None
    return date


def _get_reference_links(soup: bs, url: str) -> List[str]:
    '''
    Get the links of related articles from BS object.

    Args:
        soup (bs): BS object.
        url (str): URL of the article (for reporting exceptions).

    Returns:
        List[str]: List of links. Return 0 elements if no links or None in case of exception.
    '''
    try:
        links_frame = soup.find('div', class_='frame_news_article_adapt')
        links = []
        if links_frame:
            links = links_frame.find_all('a')
            links = set([urlparse.urlparse(URL_MAIN + link['href'].strip()).geturl() for link in links])
            links_frame.decompose()
    except AttributeError as e:
        logger.warning(helper._message(f'Failed to fetch links at URL {url}', e))
        # raise SystemExit(e)
        return None
    return list(links)


def _get_body(soup: bs, url: str) -> str:
    '''
    Get the article body from BS object.

    Args:
        soup (bs): BS object.
        url (str): URL of the article (for reporting exceptions).

    Returns:
        str: Article body (text) or None in case of exception.
    '''
    try:
        body = soup.find('div', class_='body_article_bl')
        body = re.sub(r'\s+', ' ', body.get_text().strip())
    except AttributeError as e:
        logger.error(helper._message(f'Failed to fetch the body text at {url}', e))
        # raise SystemExit(e)
        return None
    return body


def _get_tags(soup: bs, url: str) -> List[str]:
    '''
    Get the tags for the article from BS object. It is assumed that articles are always with tags.
    (FIX IF NEEDED)

    Args:
        soup (bs): BS object.
        url (str): URL of the article (for reporting exceptions).

    Returns:
        List[str]: List of tags or None in case of exception.
    '''
    try:
        tags = soup.find('div', class_='keywords_bl').find_all('a')
        tags = [re.sub(r'\s+', ' ', t.get_text().strip()) for t in tags]
    except AttributeError as e:
        logger.warning(helper._message(f'Failed to fetch tags at URL {url}', e))
        # raise SystemExit(e)
        return None
    return tags


def _get_author(soup: bs, url: str) -> Optional[str]:
    '''
    Get the author of the article if exists from BS object.

    Args:
        soup (bs): BS object.
        url (str): URL of the article (for reporting exceptions).

    Returns:
        Optional[str]: Return author (text) or None if not found or in case of exception.
    '''
    try:
        author = soup.find('div', class_='data_author_bl').find('a')
        author = re.sub(r'\s+', ' ', author.get_text().strip())
    except AttributeError as e:
        logger.warning(helper._message(f'Failed to fetch author at URL {url}', e))
        # raise SystemExit(e)
        return None
    return author


def get_article(response: requests.Response) -> Dict[str, str]:
    '''
    Retrieving article data given the response from article URL.

    Args:
        response (requests.Response): Response object of the article URL.

    Returns:
        Dict[str, str]: Dictionary with elements of the article.
    '''
    soup = bs(response.content, 'html.parser')
    res = {}
    res['url'] = response.url

    title = _get_title(soup, response.url)
    date = _get_date(soup, response.url)
    links = _get_reference_links(soup, response.url)
    body = _get_body(soup, response.url)
    if not all([title, date, body]):
        logger.error(helper._message(f'Failed to fetch the article at URL {response.url}'))
        return None
    tags = _get_tags(soup, response.url)
    author = _get_author(soup, response.url)

    res['title'] = title
    res['date'] = date
    res['body'] = body
    if len(links) > 0:
        res['links'] = links
    if len(tags) > 0:
        res['tags'] = tags
    if author:
        res['author'] = author
    logger.info(helper._message(f'Retrieved article at URL: {response.url}'))

    return res
