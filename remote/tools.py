import json

__author__ = 'Lorenzo'


def test_integrity(res):
    try:
        res = json.loads(res)
        return res
    except Exception:
        print "the endpoint response was in the wrong format or status 400 or 500"
        print res
        assert False
