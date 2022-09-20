'''
Module for testing ORM.

Author: Dauren Baitursyn
Date: 11.07.21
'''

import unittest
import os

from db import models

import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from dotenv import load_dotenv

load_dotenv()


class TestORM(unittest.TestCase):
    a1 = {
        'url': 'url1',
        'title': 'title1',
        'date': '2020-01-01',
        'body': 'body1',
        'author': 'author1'
    }
    a2 = {
        'url': 'url2',
        'title': 'title2',
        'date': '2020-01-01',
        'body': 'body2'
    }
    a3 = {
        'url': 'url3',
        'title': 'title3',
        'date': '2020-01-01',
        'body': 'body3'
    }
    a1d = {
        'url': 'url1',
        'title': 'title2',
        'date': '2020-01-01',
        'body': 'body1'
    }
    aInv = {}

    urls1 = {'url_main': 'url1', 'url_other': 'url2'}
    urls2 = {'url_main': 'url1', 'url_other': 'url3'}
    urls3 = {'url_main': 'url3', 'url_other': 'url2'}
    urls1d = {'url_main': 'url1', 'url_other': 'url2'}
    urlsInv1 = {'url_main': 'invalid1', 'url_other': 'url1'}
    urlsInv2 = {'url_main': 'url1', 'url_other': 'invalid2'}
    urlsInv3 = {'url_main': 'invalid1', 'url_other': 'invalid2'}
    urlsInv4 = {}

    tag1 = {'url': 'url1', 'tag': 'tag1'}
    tag2 = {'url': 'url1', 'tag': 'tag2'}
    tag3 = {'url': 'url2', 'tag': 'tag3'}
    tag1d = {'url': 'url1', 'tag': 'tag1'}
    tagInv1 = {'url': 'invalid1', 'tag': 'tag1'}
    tagInv2 = {}

    def setUp(self):
        self.engine = create_engine(os.getenv('DB_URI_TEST'))
        models.Base.metadata.drop_all(self.engine)
        models.Base.metadata.create_all(self.engine)
        self.session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
        )
        models.Base.query = self.session.query_property()

    def test_articles(self):
        '''
        Testing ORM operations with articles models.
        '''
        s = self.session()

        models.insert_article(self.a1, s)
        models.insert_article(self.a2, s)
        models.insert_article(self.a3, s)
        s.commit()
        r = s.query(models.Article).all()
        self.assertEqual(len(r), 3)
        self.assertNotEqual(r[0].id, None)
        self.assertNotEqual(r[1].id, None)
        self.assertNotEqual(r[2].id, None)

        models.insert_article(self.a1d, s)
        self.assertRaises(sqlalchemy.exc.IntegrityError, s.commit)
        s.rollback()

        self.assertEqual(models.insert_article(self.aInv, s), None)

    def test_links(self):
        '''
        Testing ORM operations with links models.
        '''
        s = self.session()
        models.insert_article(self.a1, s)
        models.insert_article(self.a2, s)
        models.insert_article(self.a3, s)
        s.commit()

        models.insert_link(self.urls1, s)
        models.insert_link(self.urls2, s)
        models.insert_link(self.urls3, s)
        s.commit()
        links = s.query(models.ArticleLink).all()
        self.assertEqual(len(links), 3)
        self.assertNotEqual(links[0].id, None)
        self.assertNotEqual(links[1].id, None)
        self.assertNotEqual(links[2].id, None)

        models.insert_link(self.urls1d, s)
        self.assertRaises(sqlalchemy.exc.IntegrityError, s.commit)
        s.rollback()

        self.assertEqual(models.insert_link(self.urlsInv1, s), None)
        self.assertEqual(models.insert_link(self.urlsInv2, s), None)
        self.assertEqual(models.insert_link(self.urlsInv3, s), None)
        self.assertEqual(models.insert_link(self.urlsInv4, s), None)

    def test_tags(self):
        '''
        Testing ORM operations with tags models.
        '''
        s = self.session()
        models.insert_article(self.a1, s)
        models.insert_article(self.a2, s)
        s.commit()

        models.insert_tag(self.tag1, s)
        models.insert_tag(self.tag2, s)
        models.insert_tag(self.tag3, s)
        s.commit()
        t = s.query(models.ArticleTag).all()
        self.assertEqual(len(t), 3)
        self.assertNotEqual(t[0].id, None)
        self.assertNotEqual(t[1].id, None)
        self.assertNotEqual(t[2].id, None)

        models.insert_tag(self.tag1d, s)
        self.assertRaises(sqlalchemy.exc.IntegrityError, s.commit)
        s.rollback()

        self.assertEqual(models.insert_tag(self.tagInv1, s), None)
        self.assertEqual(models.insert_tag(self.tagInv2, s), None)

    def tearDown(self):
        self.session.remove()
        models.Base.metadata.drop_all(self.engine)
