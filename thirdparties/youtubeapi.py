import unittest
import json

__author__ = 'Lorenzo'

from config.secret import YOUTUBE_KEY

url = 'https://www.googleapis.com/youtube/v3/search'
params= {
    'part': 'id, snippet',
    'q': ['space+exploration', 'space race', 'space', 'astrophysics', 'astronomy'],
    'publishedAfter': '2005-01-01T00:00:00Z',
    'publishedBefore': '2005-01-01T00:00:00Z',
    'key': YOUTUBE_KEY
}

def fetch_data():
    import urllib
    data = urllib.urlencode({
            'part': params['part'],
            'q': params['q'][0],
            'maxResult': 3,
            'key': params['key']
        })
    request = url + '?' +data
    response = urllib.urlopen(
        request
    )
    return response.read()

def store_video(obj):
    print obj

def store_response(resp):
    for video in resp.items:
        store_video(video)


response = fetch_data()

#store_response(response)

# note: pageToken = response.nextPageToken
print json.loads(response)
