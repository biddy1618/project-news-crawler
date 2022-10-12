'''
Auxilary function for async crawler.

Author: Dauren Baitursyn
Date: 12.10.22
'''
import logging
import asyncio
import re

import urllib.parse as urlparse
from bs4 import BeautifulSoup as bs

import helper

logger = logging.getLogger(__name__)
URL_MAIN = 'https://www.inform.kz'


async def get_url(session, url):
    '''
    Function to perform GET request on the given url using the session object.

    Args:
        session (aiohttp.ClientSession): Session object.
        url (str): URL to fetch.

    Returns:
        str: Response content in string format.
    '''
    try:
        async with session.get(url) as response:
            assert response.status == 200
            return await response.text()
    except AssertionError as e:
        logger.error(helper._message(f'Failed to fetch article at URL {url}', e))
        return None
    

async def get_pages(session, url):
    '''
    Return the contents of main pages from pagination links from the main page.

    Args:
        session (aiohttp.ClientSession): Session object.
        url (str): URL for specific date.

    Returns:
        list: List of pages in string format (responses).
    '''
    content = get_url(url)

    try:
        soup = bs(content, 'html.parser')
        links_pages = soup.find('p', class_='pagination').find_all('a')
        links_pages = set([urlparse.urlparse(URL_MAIN + link['href'].strip()).geturl() for link in links_pages])
        links_pages = list(links_pages)
    except AttributeError as e:
        logger.error(helper._message(f'Failed to fetch articles page links at URL {url}', e))
        links_pages = []


    response_pages = await asyncio.gather(*[
        get_url(session, link) for link in links_pages
    ])

    response_pages = [content] + response_pages
    response_pages = [page for page in response_pages if page is not None]
    logger.info(helper._message(f'Retrieved {len(response_pages)} pages from {url} successfully.'))

    return response_pages


async def get_article_links(session, pages, url):
    '''
    Get articles links given the response objects of the pages in string format.

    Args:
        session (aiohttp.ClientSession): Session object.
        pages (list): List of pages (responses) in string format.
        url (str): URL of main page (for debugging purposes).

    Returns:
        list: List of tuples of articles and its URL in string format (responses).
    '''
    links_articles_all = []
    for page in pages:
        try:
            soup = bs(page, 'html.parser')


            links_articles = soup.find('div', class_='news-list__col').find_all('a')
            links_articles = set([urlparse.urlparse(URL_MAIN + link['href'].strip()).geturl() for link in links_articles])
        except AttributeError as e:
            logger.error(helper._message(f'Failed to extract links to articles at {url}.', e))
            links_articles = []
        links_articles_all.extend(list(links_articles))

    response_articles = await asyncio.gather(*[
        get_url(session, link) for link in links_articles_all
    ])
    response_articles = [(article, url_article) for article, url_article in zip(response_articles, links_articles_all) if article is not None]
    logger.info(helper._message(f'Retrieved {len(response_articles)} articles from {url} successfully.'))

    return response_articles


def retrieve_data(article, url):
    '''
    Get data from the response content of article.

    Args:
        article (str): String representation of the article content.
        url (str): URL of the article (for debugging purposes).

    Returns:
        dict: Dictionary object with scraped fields.
    '''
    soup = bs(article, 'html.parser')

    try:
        title = soup.find('div', class_='title_article_bl')
        title = re.sub(r'\s+', ' ', title.get_text().strip())
    except AttributeError as e:
        logger.error(helper._message(f'Failed to fetch title at URL {url}', e))
        return None

    try:
        date = soup.find('div', class_='time_article_bl')
        date = re.sub(r'\s+', ' ', date.get_text().strip())
    except AttributeError as e:
        logger.error(helper._message(f'Failed to fetch date at URL {url}', e))
        return None
    
    try:
        links = []
        links_frame = soup.find('div', class_='frame_news_article_adapt')
        if links_frame:
            links = links_frame.find_all('a')
            links = set([urlparse.urlparse(URL_MAIN + link['href'].strip()).geturl() for link in links])
            links = list(links)
            links_frame.decompose()
    except AttributeError as e:
        logger.warning(helper._message(f'Failed to fetch links at URL {url}', e))
        links = []
    
    try:
        body = soup.find('div', class_='body_article_bl')
        body = re.sub(r'\s+', ' ', body.get_text().strip())
    except AttributeError as e:
        logger.error(helper._message(f'Failed to fetch the body text at {url}', e))
        return None
    
    try:
        tags = soup.find('div', class_='keywords_bl').find_all('a')
        tags = [re.sub(r'\s+', ' ', t.get_text().strip()) for t in tags]
    except AttributeError as e:
        logger.warning(helper._message(f'Failed to fetch tags at URL {url}', e))
        tags = []
    
    try:
        author = soup.find('div', class_='data_author_bl').find('a')
        author = re.sub(r'\s+', ' ', author.get_text().strip())
    except AttributeError as e:
        logger.warning(helper._message(f'Failed to fetch author at URL {url}', e))
        author = None
    
    res = {
        'title': title,
        'date': date,
        'body': body,
        'links': links,
        'tags': tags,
    }
    if author:
        res['author'] = author

    return res