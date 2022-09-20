'''
Module for testing crawler.

Author: Dauren Baitursyn
Date: 11.07.21
'''

import unittest
import random

from crawler.crawler import Crawler
import helper


class TestCrawler(unittest.TestCase):

    invalid = 'invalid'

    def setUp(self):
        self.crawler = Crawler()

    def test_dates(self):
        '''
        Testing crawler functions - generating dates.
        '''
        self.assertEqual(helper.generate_dates('invalid'), None)
        self.assertEqual(helper.generate_dates('01.01.2020', 'invalid'), None)
        self.assertEqual(helper.generate_dates('01.01.2020', '01.01.2019'), None)
        self.assertEqual(helper.generate_dates('01.01.2020', '01.01.2020'), None)

        dates = helper.generate_dates('01.01.2019', '02.01.2020')
        self.assertNotEqual(dates, None)

    def test_get_url(self):
        '''
        Testing crawler functions - getting data at URL.
        '''
        self.assertEqual(self.crawler.get_url(self.invalid), None)
        self.assertEqual(self.crawler.get_url(self.invalid, {}), None)
        self.assertEqual(self.crawler.get_url(self.invalid, {'date': self.invalid}), None)
        # Following test fails since web-site actually returns page even if the parameters are wrong
        # self.assertEqual(crawler.get_url(crawler.URL_ARCHIVE, {'date': self.invalid}), None)

    def test_crawling_and_extracting_articles(self):
        '''
        Testing crawler functions - crawling and extracting articles.
        '''
        dates = helper.generate_dates('01.01.2019', '02.01.2020')

        for d in random.sample(dates, 1):
            r = self.crawler.get_url(self.crawler.URL_ARCHIVE, {'date': d})
            self.assertEqual(r.status_code, 200)

            links = self.crawler.get_links(r)

            for link in random.sample(links, 5):
                page = self.crawler.get_url(link)
                self.assertEqual(r.status_code, 200)
                article = self.crawler.extract_article(page)

                self.assertTrue('url' in article)
                self.assertTrue('title' in article)
                self.assertTrue('date' in article)
                self.assertTrue('body' in article)

                self.assertIsInstance(article['title'], str)
                self.assertIsInstance(article['date'], str)
                self.assertIsInstance(article['body'], str)

                if 'links' in article:
                    self.assertIsInstance(article['links'], list)
                if 'tags' in article:
                    self.assertIsInstance(article['tags'], list)
                if 'author' in article:
                    self.assertIsInstance(article['author'], str)

    def tearDown(self):
        self.crawler.close()
