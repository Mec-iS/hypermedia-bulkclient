"""
Tests for ORM
"""
import time


from database.createdb import WebResource, Indexer

__author__ = 'Lorenzo'

from config.config import ENV
from remote.remote import get_curling
from remote.tools import test_integrity

from database.interfacedb import orm_new_webresource


def test_orm_get_webresource(uuid):
    """
    Query a single WebResource
    :param uuid:
    :return:
    """
    pass

def test_fetch_by_url(url):
    from database.interfacedb import orm_get_by_url

    return orm_get_by_url(WebResource, url).title

print test_fetch_by_url("http://www.space.com/30798-back-to-the-future-documentary.html")

def test_orm_fetch_webresources(limit=10, offset=0):
    """
    Query select WebResource(s)
    :param limit:
    :param offset:
    :return:
    """
    pass


def test_dumps_articles_api():
    """
    Warning: use with caution, it is resource intensive for the remote server.

Test the Articles JSON API: /articles/<version>/
"""
    _VERSION = "v04"
    print "Running test_articles"
    import urllib
    env = 'offline'  # switch to online if want to play it remotely

    base_url = ENV[env]['_SERVICE'] + "/articles/" + _VERSION + "/"

    first = get_curling(base_url)
    first = test_integrity(first)

    bookmark = first['next']
    print bookmark
    for i in range(0, 600):  # higher the second element of the interval to test more pages
        print i
        if bookmark:
            response = urllib.urlopen(bookmark).read()
            response = test_integrity(response)
            for a in response['articles']:
                print orm_new_webresource(a)

            bookmark = response['next']
            print i, bookmark
        else:
            print 'Articles finished'
            return None

# test_dumps_articles_api()


def test_orm_insertion():
    test_objects = [{"in_graph": False, "uuid": 5363672197103616, "title": "652301944141164544", "url": "https://twitter.com/BadAstronomer/status/652301944141164544", "abstract": "You got one sold already, BB.  https://t.co/wUVEVha4oP", "keywords_url": "http://hypermedia.projectchronos.eu/articles/v04/?url=https://twitter.com/BadAstronomer/status/652301944141164544", "stored": "2015-10-08T16:14:44", "published": "2015-10-09T01:57:57", "type_of": "tweet"},
                    {"in_graph": False, "uuid": 5629499534213120, "title": "", "url": "https://twitter.com/bonniegrrl/status/652281122521415681", "abstract": "", "keywords_url": "http://hypermedia.projectchronos.eu/articles/v04/?url=https://twitter.com/bonniegrrl/status/652281122521415681", "stored": "2015-10-08T16:14:44", "published": "2015-10-09T01:57:57", "type_of": "link"}]

    for t in test_objects:
        print orm_new_webresource(t)

    # fetch and test insertion
