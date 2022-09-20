'''
Module for ORM models.

Author: Dauren Baitursyn
Date: 11.07.21
'''

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Identity, UniqueConstraint
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy.inspection import inspect
from sqlalchemy.ext.declarative import declarative_base

from decimal import Decimal as D

from typing import List
import helper
import logging
import dateparser

Base = declarative_base()

logger = logging.getLogger(__name__)


class BaseH(object):

    @declared_attr
    def __tablename__(self):
        return self.__class__.__name__.lower()

    def serialize(self):
        return {c.name: getattr(self, c.name) for c in inspect(self.__class__).c}

    def update(self, data):
        for k, v in data.items():
            setattr(self, k, v)

    @staticmethod
    def serializeStatic(row):
        return {c: BaseH.checkDecimal(getattr(row, c))
                for c in row.keys()}

    @staticmethod
    def checkDecimal(val):
        return str(val) if isinstance(val, D) else val


class Article(Base, BaseH):
    __tablename__ = 'articles'

    id = Column(Integer, Identity(), primary_key=True)
    url = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    body = Column(String, nullable=False)
    author = Column(String)

    def __repr__(self):
        return f'Article: "{self.url}"'


class ArticleLink(Base, BaseH):
    __tablename__ = 'article_links'
    __table_args__ = (UniqueConstraint('id_article', 'id_article_other'),)

    id = Column(Integer, Identity(), primary_key=True)
    id_article = Column(ForeignKey('articles.id'), nullable=False)
    id_article_other = Column(ForeignKey('articles.id'), nullable=False)

    article = relationship('Article', primaryjoin='ArticleLink.id_article == Article.id')
    article1 = relationship('Article', primaryjoin='ArticleLink.id_article_other == Article.id')

    def __repr__(self):
        return f'Link: "{self.article.url}" -> "{self.article1.url}"'


class ArticleTag(Base, BaseH):
    __tablename__ = 'article_tags'
    __table_args__ = (UniqueConstraint('id_article', 'tag'),)

    id = Column(Integer, Identity(always=True, start=1, increment=1), primary_key=True)
    id_article = Column(ForeignKey('articles.id'), nullable=False)
    tag = Column(String, nullable=False)

    article = relationship('Article')

    def __repr__(self):
        return f'Tag: "{self.tag}" linked to "{self.article.url}"'


def insert_article(article: dict, session: Session) -> Article:
    '''
    Insert the article object into session stage.

    Args:
        article (dict): Dictionary with following elements: "url", "title", "date", "body", "author" (optional).
        session (Session): Session object.

    Returns:
        Article: Return SQLAlchemy ORM Article models that was staged in session.
    '''
    try:
        date = dateparser.parse(article['date'])
        a = Article(
            url=article['url'],
            title=article['title'],
            date=date,
            body=article['body'],
        )
        if 'author' in article:
            a.author = article['author']
        session.add(a)
    except KeyError as e:
        logger.error(helper._message(f'Failed to get attributes while inserting article: {article}', e))
        return None
    except DBAPIError as e:
        logger.error(helper._message(f'Error at insertion of the following article: {article}', e))
        return None

    return a


def insert_article_bulk(articles: list, session: Session) -> List[Article]:
    '''
    Staging article objects into session object. Same as "insert_article", but for the list of article objects.

    Args:
        articles (list): List of article objects.
        session (Session): Session object.

    Returns:
        List[Article]: List of SQLAlchemy ORM Article models that were staged in session.
    '''
    res = []

    for a in articles:
        res.append(insert_article(a, session))

    return res


def get_article_by_url(url: str, session: Session) -> Article:
    '''
    Get the SQLAlchemt ORM Article model given the URL.

    Args:
        url (str): URL of the desired article
        session (Session): Session object.

    Returns:
        Article: Return Article model given the URL. None in case it doesn't exist.
    '''
    a = session.query(Article).filter_by(url=url).first()
    return a


def insert_link(urls: dict, session: Session) -> ArticleLink:
    '''
    Insert the link object into session stage.

    Args:
        urls (dict): Link dicitonary with following elements: "url_main", "url_other".
        session (Session): Session object.

    Returns:
        ArticleLink: Return staged ArticleLink model. None in case of error.
    '''
    try:
        article1 = get_article_by_url(urls['url_main'], session)
        article2 = get_article_by_url(urls['url_other'], session)
    except KeyError as e:
        logger.error(helper._message(f'Failed to get URL attributes while inserting link: {urls}', e))
        return None
    try:
        link = ArticleLink(
            id_article=article1.id,
            id_article_other=article2.id
        )
        session.add(link)
    except AttributeError as e:
        logger.error(helper._message(f'Failed to find the articles IDs with URLs while inserting link: {urls}', e))
        return None
    except DBAPIError as e:
        logger.error(helper._message(f'Error at insertion of the following link: {urls}', e))
        return None

    return link


def insert_tag(url_tag: dict, session: Session) -> ArticleTag:
    '''
    Insert the tag object into session stage.

    Args:
        url_tag (dict): Tag object with following elements: "url", "tag".
        session (Session): Session object.

    Returns:
        ArticleTag: return ArticleTag model staged into session. Return None in case of error.
    '''
    try:
        article = get_article_by_url(url_tag['url'], session)
        tag = url_tag['tag']
    except KeyError as e:
        logger.error(helper._message(f'Failed to get tag attributes while inserting tag: {url_tag}', e))
        return None
    try:
        t = ArticleTag(
            id_article=article.id,
            tag=tag
        )
        session.add(t)
    except AttributeError as e:
        logger.error(
            helper._message(
                f'Failed to find the article ID with URL while inserting tag: {url_tag["url"]}',
                e))
        return None
    except DBAPIError as e:
        logger.error(helper._message(f'Error at insertion of the following link: {url_tag}', e))
        return None

    return t
