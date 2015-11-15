import json

__author__ = 'Lorenzo'

from config.config import ENV
from config.secret import CLIENT_TOKEN
from remote.remote import get_curling, post_curling

test_env = 'offline'


def get_resource(*args):
    """
    GET a resource from the datastore
    :param kind: the entity kind to get
    :param uuid: the entity uuid
    :return: a JSON representation of a resource in the datastore
    """
    kind, uuid = args
    allowed_kinds = ['webresource', 'indexer']
    if kind in allowed_kinds:
        resource = get_curling(
            ENV[test_env]['_SERVICE'] + '/datastore/' + kind,
            {
                'token': CLIENT_TOKEN,
                'retrieve': uuid
            }
        )
        return resource
    else:
        raise ValueError('get_resource: wrong kind in arguments')


def download_ids_generator(self, kind, results=(), bookmark='start'):
    """
    Recursive - Fetch and collect all the resources' ids in the datastore
    :param kind: kind of the the entities
    :param results: list of the collected ids
    :param bookmark: bookmark to fetch different datastore's pages
    :return: results list

    # USAGE
        iterated = download_ids_generator(environment='offline')
        for uuid in iterated:
             print uuid
             next(iterated)

    """
    import itertools

    to_append = get_curling(ENV[test_env]['_SERVICE'] + '/datastore/' + kind + '?index=',
                            {'token': CLIENT_TOKEN,
                             'bookmark': bookmark if bookmark != 'start' else ''})
    to_append = json.loads(to_append)

    if not to_append['next']:
        return itertools.chain(results, iter(to_append['articles']))

    return self.download_ids_generator(
        kind=kind,
        results=itertools.chain(results, iter(to_append['articles'])),
        bookmark=to_append['next']
    )


def bulk_updated():
    """
    Works with server-side chunk:
        if self.request.get('token') == _CLIENT_TOKEN:
        if name == 'correctentries' and self.request.get('skip'):
            from articlesjsonapi import memcache_webresource_query
            from datastore.models import WebResource

            query = WebResource.query()

            for q in query.fetch(500, offset=int(self.request.get('skip'))):
                try:
                    q.in_graph
                except AttributeError:
                    setattr(q, 'in_graph', False)

                try:
                    int(q.title)
                    if 'facebook.com' in q.url:
                        setattr(q, 'type_of', 'fb')
                    elif 'twitter.com' in q.url:
                        setattr(q, 'type_of', 'tweet')
                except:
                    if 'arxiv.org' in q.url:
                        setattr(q, 'type_of', 'paper')
                    elif q.title == '' and q.abstract == '':
                        if q.url.endswith(('jpg', 'jpeg', 'png', 'mp3', 'mp4', 'm4v')):
                            setattr(q, 'type_of', 'media')
                        elif q.url.endswith('pdf'):
                            setattr(q, 'type_of', 'pdf')
                        else:
                            setattr(q, 'type_of', 'link')
                    else:
                        setattr(q, 'type_of', 'feed')

                q.put()
                print q.to_dict()
    :return:
    """

    i = 0
    while True:
        t = get_curling(
            ENV['online']['_SERVICE'] + '/datastore/correctentries',
            {
                'token': CLIENT_TOKEN,
                'skip': i
            }
        )

        print i
        if i + 500 > 20500:
            break

        i += 500

bulk_updated()