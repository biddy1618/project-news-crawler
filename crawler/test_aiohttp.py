import aiohttp
import asyncio

from bs4 import BeautifulSoup as bs
import urllib.parse as urlparse

URL_MAIN = 'https://www.inform.kz'


async def _get_url(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        # given the date, get the first page
        url_links = 'https://www.inform.kz/ru/archive?date=01.05.2020'
        response_main = await _get_url(session, url_links)

        # get pagination links
        soup = bs(response_main, 'html.parser')
        links = soup.find('p', class_='pagination').find_all('a')
        links = set([urlparse.urlparse(URL_MAIN + link['href'].strip()).geturl() for link in links])
        links = list(links)
        print(f'Number of links: {len(links)}')

        results = await asyncio.gather(*[
            _get_url(session, link) for link in links
        ])

        return results

results = asyncio.run(main())

for r in results:
    print(r[:20])
