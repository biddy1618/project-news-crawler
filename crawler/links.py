'''
Module for crawling links given the Response object of the artilce links page.
Function `get_links` uses locally defined functions:
`_extract_page`
Function `_get_links`

Author: Dauren Baitursyn
Date: 11.07.21
'''

import requests
import logging
import urllib.parse as urlparse


from bs4 import BeautifulSoup as bs
from typing import List

import helper


URL_MAIN = 'https://www.inform.kz'
logger = logging.getLogger(__name__)


def _get_links(response: requests.Response) -> List[str]:
    '''
    Retrieving links given the response object of the archive list of articles for
    specific date.

    Args:
        body (requests.Response): Response object containing links to articles for a given date.

    Returns:
        List[str]: List of extractred article links given the reponse or None in case of exception.
    '''
    soup = bs(response.content, 'html.parser')
    try:
        links = soup.find('div', class_='news-list__col').find_all('a')
        links = set([urlparse.urlparse(URL_MAIN + link['href'].strip()).geturl() for link in links])
    except AttributeError as e:
        logger.error(helper._message(f'Failed to extract links to articles at {response.url}.', e))
        # raise SystemExit(e)
        return None
    logger.info(helper._message(f'Retrieved article links from {response.url} successfully.'))
    return list(links)


def get_pages(response: requests.Response) -> List[str]:
    '''
    Retrieving article page links from first page for the some particular date.
    Note: call this function for the first page from particular date to retieve the article pages
    for that particular date.

    Args:
        response (requests.Response): Response object of the first page.

    Returns:
        List[str]: Links for the article pages or None in case of exception.
    '''
    soup = bs(response.content, 'html.parser')
    try:
        links = soup.find('p', class_='pagination').find_all('a')
        links = set([urlparse.urlparse(URL_MAIN + link['href'].strip()).geturl() for link in links])
    except (AttributeError, IndexError, ValueError, TypeError) as e:
        logger.error(helper._message(f'Failed to fetch articles page links at URL {response.url}', e))
        # raise SystemExit(e)
        return []
    logger.info(helper._message(f'Retrieved article page links from {response.url} successfully'))
    return list(links)


def get_links(responses: List[requests.Response]) -> List[str]:
    '''
    Get the list of article URLs for specific date.

    Args:
        responses (List[requests.Response]): List of response object for all pages for specific date.

    Returns:
        List[str]: List of URLs for articles for the specific date or None in case of exception.
    '''
    articles = []
    for response in responses:
        articles.extend(_get_links(response))
    return articles
