"""
Collect methods to be used to operate the triple store
using the dedicated handler on the server.

SERVICE/triplestore/<perform:[a-z]+>
perform values > ('dump', 'monitor')
"""

__author__ = 'Lorenzo'


def store_webresources():
    """
    Order a dump of WebResource objects from the datastore
    to the Triple Store

    :return: None
    """

    from remote.remote import post_curling
    from config.config import ENV
    from config.secret import CLIENT_TOKEN

    # invoke a POST to store a batch of objects in the
    # triple store
    post_curling(
        ENV['offline']['_SERVICE'] + '/triplestore/dump',
        {'token': CLIENT_TOKEN, 'batch': 25},
        display=True
    )

if __name__ == '__main__':
    store_webresources()