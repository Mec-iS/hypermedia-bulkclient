"""
Provide an interface for common database operations
"""


from database.createdb import WebResource, Indexer
from config.config import DBSession
from sqlalchemy.exc import IntegrityError, InvalidRequestError

__author__ = 'Lorenzo'


def orm_new_webresource(obj):
    """
    Store a new Web resource in the database from a dictionary.

    For tests see unittesting/tests_sqlalchemy.py

    :param obj: dict()
    :return: dict()
    """
    session = DBSession()

    try:
        assert isinstance(obj, dict)
    except AssertionError as e:
        raise ValueError('orm_new_webresource: Input must be a dictionary' + str(e))

    resource = WebResource(
        **({k: a for k, a in obj.items() if k in WebResource.__table__.columns})
    )
    try:
        session.add(resource)
        session.commit()
    except Exception as e:
        session.rollback()
        print str(e)
        return None

    return resource


def orm_get_by_pk(cls, pk):
    """

    Note: https://gist.github.com/podhmo/4345741
    :param cls:
    :param pk:
    :return:
    """
    session = DBSession()
    return session.query(cls).filter(cls.id == pk).one()


def orm_get_by_url(cls, url):
    """

    Note: https://gist.github.com/podhmo/4345741
    :param cls:
    :param url:
    :return:
    """
    session = DBSession()
    return session.query(cls).filter(cls.url == url).one()


