'''
Module for crawler class.

Author: Dauren Baitursyn
Date: 11.07.21
'''

import requests
import logging
import time
import json
import re

import urllib.parse as urlparse


from bs4 import BeautifulSoup as bs
from typing import Dict, List, Optional

import helper

logger = logging.getLogger(__name__)


class Crawler():
    '''
    Generic class defining crawler.
    '''
    def __init__(self):
        self.URL_MAIN = 'https://www.inform.kz'
        self.URL_ARCHIVE = 'https://www.inform.kz/ru/archive'
        self.TIMEOUT = 5
        self.session = requests.Session()

    def close(self):
        '''
        Close the session associated with the crawler.
        '''
        self.session.close()

    def get_url(self, url: str, params: Dict[str, str] = None) -> requests.Response:
        '''
        Fetch the URL provided and return response object.

        Args:
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
                r = self.session.get(url, params=params, timeout=self.TIMEOUT)
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

    def _extract_links(self, response: requests.Response) -> List[str]:
        '''
        Retrieving links given the response object.

        Args:
            body (requests.Response): Response object containing links to articles.

        Returns:
            List[str]: List of extractred article links given the reponse or None in case of exception.
        '''
        soup = bs(response.content, 'html.parser')
        link_divs = soup.find_all('div', class_='lenta_news_block')
        try:
            links = [d.li.a['href'].strip() for d in link_divs]
        except AttributeError as e:
            logger.error(helper._message(f'Failed to extract links to articles at {response.url}.', e))
            # raise SystemExit(e)
            return None
        logger.info(helper._message(f'Retrieved article links from {response.url} successfully.'))
        return [urlparse.urlparse(self.URL_MAIN + link).geturl() for link in links]

    def _extract_pages(self, response: requests.Response) -> List[str]:
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
            pages = soup.find('p', class_='pagination')
            pages = pages.find_all('a')
            pi = pages[0].getText().strip()
            pl = pages[-1].getText().strip()
            parsed_url = urlparse.urlparse(response.url)
            pages = [parsed_url._replace(path=f'/ru/archive/{str(i)}').geturl() for i in range(int(pi), int(pl) + 1)]
        except (AttributeError, IndexError, ValueError, TypeError) as e:
            logger.error(helper._message(f'Failed to fetch articles page links at URL {response.url}', e))
            # raise SystemExit(e)
            return []
        logger.info(helper._message(f'Retrieved article page links from {response.url} successfully'))
        return pages

    def get_links(self, response: requests.Response) -> List[str]:
        '''
        Get the list of URLs for the articles given the response object from particular URL of specific date.

        Args:
            response (requests.Response): Response object of the first page.

        Returns:
            List[str]: List of URLs for articles for the specific date or None in case of exception.
        '''
        articles = self._extract_links(response)
        for link in self._extract_pages(response):
            r = self.get_url(link)
            articles.extend(self._extract_links(r))
        return articles

    def _get_title(self, soup: bs, url: str) -> str:
        '''
        Get the title of the article from BS object.

        Args:
            soup (bs): BS object.
            url (str): URL of the article (for reporting exceptions).

        Returns:
            str: Title of the article or None in case of exception.
        '''
        try:
            title = soup.find('div', class_='article_title')
            title = title.getText().strip()
        except AttributeError as e:
            logger.error(helper._message(f'Failed to fetch title at URL {url}', e))
            # raise SystemExit(e)
            return None
        return title

    def _get_date(self, soup: bs, url: str) -> str:
        '''
        Get the date of the article from BS object.

        Args:
            soup (bs): BS object.
            url (str): URL of the article (for reporting exceptions).

        Returns:
            str: Date of the article or None in case of exception.
        '''
        try:
            date = soup.find('div', class_='date_public_art')
            date = date.getText().strip()
        except AttributeError as e:
            logger.error(helper._message(f'Failed to fetch date at URL {url}', e))
            # raise SystemExit(e)
            return None
        return date

    def _get_reference_links(self, soup: bs, url: str) -> List[str]:
        '''
        Get the links of related articles from BS object.

        Args:
            soup (bs): BS object.
            url (str): URL of the article (for reporting exceptions).

        Returns:
            List[str]: List of links. Return 0 elements if no links or None in case of exception.
        '''
        try:
            links = soup.find('div', class_='frame_news_article')
            res = set()
            if links:
                for a in links.find_all('a'):
                    res.add(urlparse.urlparse(self.URL_MAIN + a['href']).geturl())
                links.decompose()
        except AttributeError as e:
            logger.error(helper._message(f'Failed to fetch links at URL {url}', e))
            # raise SystemExit(e)
            return None
        return list(res)

    def _decompose_quotes(self, soup: bs, url: str) -> None:
        '''
        Decomposes some elements for clear retrieval of the article body.

        Args:
            soup (bs): BS object.
            url (str): URL of the article (for reporting exceptions).
        '''
        try:
            quotes = soup.find_all('blockquote', class_='instagram-media')
            if quotes:
                for q in quotes:
                    q.decompose()
        except AttributeError as e:
            logger.error(helper._message(f'Failed to decompose quotes at URL {url}', e))
            # raise SystemExit(e)

    def _get_body(self, soup: bs, url: str) -> str:
        '''
        Get the article body from BS object.

        Args:
            soup (bs): BS object.
            url (str): URL of the article (for reporting exceptions).

        Returns:
            str: Article body (text) or None in case of exception.
        '''
        try:
            body = soup.find('div', class_='article_news_body')
            body = body.getText().strip()
            body = re.sub(' +', ' ', body)
            body = re.sub('\r', '\n', body)
            body = re.sub('\n +', '\n', body)
            body = re.sub(' +\n', '\n', body)
            body = re.sub('\n+', '\n', body)
        except AttributeError as e:
            logger.error(helper._message(f'Failed to fetch the body text at {url}', e))
            # raise SystemExit(e)
            return None
        return body

    def _get_tags(self, soup: bs, url: str) -> List[str]:
        '''
        Get the tags for the article from BS object. It is assumed that articles is always with tags.
        (FIX IF NEEDED)

        Args:
            soup (bs): BS object.
            url (str): URL of the article (for reporting exceptions).

        Returns:
            List[str]: List of tags or None in case of exception.
        '''
        try:
            tags = soup.find('div', class_='keyword_art')
            tags = [t.strip() for t in tags.getText().split('#') if len(t.strip()) > 0]
        except AttributeError as e:
            logger.error(helper._message(f'Failed to fetch tags at URL {url}', e))
            # raise SystemExit(e)
            return None
        return tags

    def _get_author(self, soup: bs, url: str) -> Optional[str]:
        '''
        Get the author of the article if exists from BS object.

        Args:
            soup (bs): BS object.
            url (str): URL of the article (for reporting exceptions).

        Returns:
            Optional[str]: Return author (text) or None if not found or in case of exception.
        '''
        try:
            author = soup.find('p', class_='name_p')
            if author:
                author = author.getText().strip()
        except AttributeError as e:
            logger.error(helper._message(f'Failed to fetch author at URL {url}', e))
            # raise SystemExit(e)
            return None
        return author

    def extract_article(self, response: requests.Response) -> Dict[str, str]:
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

        title = self._get_title(soup, response.url)
        date = self._get_date(soup, response.url)
        links = self._get_reference_links(soup, response.url)
        self._decompose_quotes(soup, response.url)
        body = self._get_body(soup, response.url)
        if not all([title, date, body]):
            logger.error(helper._message(f'Failed to fetch the article at URL {response.url}'))
            return None
        tags = self._get_tags(soup, response.url)
        author = self._get_author(soup, response.url)

        res['title'] = title
        res['date'] = date
        if len(links) > 0:
            res['links'] = links
        res['body'] = body
        if len(tags) > 0:
            res['tags'] = tags
        if author:
            res['author'] = author
        logger.info(helper._message(f'Retrieved article at URL: {response.url}'))

        return res

    def crawl_for_date(self, date: str, log_every: int = None) -> dict:
        '''
        Retrieve articles for the given date.

        Args:
            date (str): Date in format "dd.mm.yyyy".
            log_every (int, optional): Log message every nth retrieved record.
                Defaults to None in which case doesn't log.

        Returns:
            dict: Dictionary with articles, links and tags retrieved.
        '''
        articles = []
        links = []
        tags = []
        r = self.get_url(self.URL_ARCHIVE, {'date': date})

        url_links = self.get_links(r)
        logger.info(helper._message(f'Retrieving {len(url_links)} articles for the date: {date}'))
        for i, l in enumerate(url_links):
            page = self.get_url(l)
            article = self.extract_article(page)
            if article is None:
                continue
            articles.append(article)
            if 'links' in article:
                for link in article['links']:
                    url_link = {'url_main': article['url'], 'url_other': link}
                    links.append(url_link)
            if 'tags' in article:
                for t in article['tags']:
                    tag = {'url': article['url'], 'tag': t}
                    tags.append(tag)
            if log_every and i+1 % log_every == 0:
                logger.info(helper._message(f'Retrieved {log_every} articles.'))

        logger.info(helper._message('Retrieved all articles.'))

        return {
            'articles': articles,
            'links': links,
            'tags': tags
        }


def crawl_and_save_to_file(start_date: str, end_date: str = None) -> None:
    '''
    Crawl data for the given date(s) and save it to file system.

    Args:
        start_date (str): Start date to crawl.
        s (sqlalchemy.orm.Session): Session object through which writing to DB is performed.
        end_date (str, optional): End date to crawl. Defaults to None.
    '''
    crawler = Crawler()
    dates = helper.generate_dates(start_date, end_date)
    final = {}
    for d in dates:
        final[d] = crawler.crawl_for_date(date=d)
        # final[d] = data['articles']

    crawler.close()
    with open('test.json', 'w', encoding='utf8') as json_file:
        json.dump(final, json_file, ensure_ascii=False)
