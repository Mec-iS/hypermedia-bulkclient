import unittest
import json

__author__ = 'Lorenzo'

from client_GET import get_resource


class GETsingleResource(unittest.TestCase):
    tests_data = {
        'offline': {
            'webresource': [5135269057527808, 5138567592411136, 5381559662149632],
            'indexer': [4509646941323264, 4549229359923200, 4597607871545344]
        },
        'online': {
            'webresource': [5449136140713984, 6745872666722304, 6480396711624704, 6310096426500096, 5063593569550336],
            'indexer': [4504469089812480, 4505341370826752, 4506188150472704]
        }
    }

    def test_get_WebResource(self, env='offline'):
        for uuid in self.tests_data[env]['webresource']:
            res = get_resource('webresource', uuid)
            res = json.loads(res)
            print res
            # check if response has all the needed properties
            assert False if not all(
                k in ['in_graph', 'abstract', 'title', 'uuid',
                      'published', 'url', 'keywords_url', 'stored', 'type_of']
                for k in res.keys()) else True

    def test_get_Indexer(self, env='offline'):
        for uuid in self.tests_data[env]['indexer']:
            res = get_resource('indexer', uuid)
            res = json.loads(res)
            print res
            assert False if not all(k in ['keyword', 'uuid'] for k in res.keys()) else True

    def runTest(self):
        run = GETsingleResource()
        run.test_get_WebResource()
        run.test_get_Indexer()
