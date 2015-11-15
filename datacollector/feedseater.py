"""
Script to dump locally datastore's resources
"""

import os
from bs4 import BeautifulSoup
import feedparser

__author__ = 'Lorenzo'


class FeedsEater(object):
    """
    A crawler for feeds
    """
    def __init__(self):
        self.links = self.load_links()

    def run(self):
        print self.links
        self.store_feeds()

    @staticmethod
    def load_links():
        """
        Loads RSS links from a local file. They are in an XML file with tag <outline/>
        :return: A list of URLs of RSS-feeds
        """

        feeds_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'thirdparties', 'files', 'newsfox.xml')
        print feeds_file
        with open(feeds_file) as f:
            markup = f.read()
        body = BeautifulSoup(markup, "lxml-xml").body
        outlines = body.find_all('outline')
        links = []
        for o in outlines:
            try:
                links.append(str(o['xmlUrl']))
            except KeyError as e:
                pass
            except Exception as e:
                raise e
        return links

    @staticmethod
    def read_feed(ln):
        """
        Parse a link with feedparser library.
        :param ln: a link to a RSS-feed
        :return: a list of dictionaries containing news from the feed
        """
        #start = time.time()
        feed = feedparser.parse(ln)

        #if time.time() - start < 30:

        if feed and isinstance(feed, list):
            return feed
        elif isinstance(feed, dict) and "entries" in feed:
            return feed["entries"]
        else:
            print ValueError('No links. Or cannot parse them in: ' + str(ln))
            return None

    def store_feeds(self):
        """
    Take a feed's url from the cached list and fetch posts
    :param args: no arguaments at the moment
    :return: None
    """

        for l in self.links:
            entries = self.read_feed(l)
            if entries:
                for entry in entries:
                    #
                    # Store feed
                    #
                    self.store_it(entry)
                print "Feed stored: " + str(l)
            else:
                print "This Feed has no entries" + str(l)
        return None

    @staticmethod
    def store_it(entry):
        """
        Translate feed entry into database object and store into SQL
        :param entry: an entry from a feedparser object
        """
        # if obj.url not in table WebResource
        from database.interfacedb import orm_new_webresource
        from time import localtime
        from datetime import datetime

        database_obj = {}

        from unidecode import unidecode
        try:
            database_obj['title'] = unidecode(unicode(" ".join(entry['title'].split())))
        except:
            database_obj['title'] = " ".join(entry['title'].encode('ascii', 'replace').split())

        if str(entry['link']).endswith('pdf'):
            database_obj['type_of'] = 'pdf'
        elif 'arxiv.com' in str(entry['link']):
            database_obj['type_of'] = 'paper'
        else:
            database_obj['type_of'] = 'feed'

        database_obj['url'] = str(entry['link'])

        database_obj['stored'] = datetime(*localtime()[:6])
        database_obj['published'] = datetime(*entry['published_parsed'][:6]) \
            if 'published_parsed' in entry.keys() \
            else database_obj['stored']

        if 'summary' in entry:
            abstract = entry['summary'].replace('\n\n', ' ').replace('\r\r', ' ').replace('\n', ' ')
            try:
                database_obj['abstract'] = unidecode(unicode(" ".join(abstract.strip().split()))) if entry['summary'] is not None else ""
            except:
                database_obj['abstract'] = " ".join(abstract.strip().encode('ascii', 'replace').split()) if entry['summary'] is not None else ""
        else:
            database_obj['abstract'] = ""

        try:
            inserted = orm_new_webresource(database_obj)
        except Exception as e:
            print Exception('FeedsEater.store_it(): ' + str(e))
            return None

        print 'media_content' in entry, 'links' in entry

        # if insert was successful
        if inserted:
            if 'media_content' in entry and len(entry.media_content) != 0:
                for obj in entry.media_content:
                    # store image or video as child
                    try:
                        m = {
                            "url": obj['url'] if 'url' in obj else obj['href'],
                            "published": inserted.published,
                            "parent_id": inserted.id,
                            "title": '',
                            "abstract": '',
                            "type_of": 'media'
                        }
                        orm_new_webresource(m)
                        print "media stored"
                    except:
                        pass
            elif 'links' in entry and len(entry.links) != 0:
                # store link as child
                for obj in entry.links:
                    try:
                        m = {
                            "url": obj['url'] if 'url' in obj else obj['href'],
                            "published": inserted.published,
                            "parent_id": inserted.id,
                            "title": '',
                            "abstract": '',
                            "type_of": 'media' if obj.url.endswith(('jpg', 'jpeg', 'png', 'mp3', 'mp4', 'm4v')) else 'link'
                        }
                        orm_new_webresource(m)
                        print m['type_of'] + " stored"
                    except:
                        pass

        return inserted

def dump_feeds():
    pass
