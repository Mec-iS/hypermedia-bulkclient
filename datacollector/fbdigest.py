import urllib
import json
import time
from datetime import datetime

__author__ = 'Lorenzo'

from config.secret import fb_appid, fb_secret


class FbDigest(object):
    """
    A crawler for FB posts
    """
    def __init__(self):
        self.token = self.generate_token()
        self.aliases = ['GuntersSpacePage', 'SETIInstitute', 'planetarysociety']
        self.endpoint = 'https://graph.facebook.com/{}/posts?{}&limit=20'

    def run(self):
        try:
            [
                self.execute_task(self.endpoint.format(a, self.token), a)
                for a in self.aliases
            ]  # fetch wall posts for each alias
        except Exception as e:
            raise Exception('FBStore Handler - Error in get(): ' + str(e))

    @staticmethod
    def generate_token():
        """
        Generate FB API token, needed to access the REST API
        :return: 'access_token=<token>'
        """
        url = 'https://graph.facebook.com/oauth/access_token'
        params = {
            'client_id': fb_appid,
            'client_secret': fb_secret,
            'grant_type': 'client_credentials'
        }
        url = url + '?' + urllib.urlencode(params)
        print url
        response = urllib.urlopen(url)
        return str(response.read())

    def execute_task(self, *args):
        """
        Store post, also recursively if response contains paging.
        Storing method: see WebResource.store_fb_post() in models.
        :param args: url of a post and the alias of the page that holds it
        :return: None
        """
        url, alias = args

        def get_wall_recursive(url):
            response = urllib.urlopen(url)
            response = json.loads(response.read())
            if 'error' not in response.keys():
                for o in response['data']:
                    self.store_fb_post(alias, o)
            else:
                from main.errors import RESTerror
                raise RESTerror('get_wall_recursive(): FB API error')

            if 'paging' not in response.keys() or not response['paging']['next']:
                return None

            return get_wall_recursive(response['paging']['next'])

        return get_wall_recursive(url)

    @classmethod
    def store_fb_post(cls, alias, obj):
        from database.interfacedb import orm_new_webresource

        if 'message' in obj.keys():
            new_post = {
                'title': obj['id'].split('_')[1]
            }
            new_post['url'] = 'https://www.facebook.com/' + alias + '/posts/' + new_post['title']

            published = str(obj['created_time'][0:19])
            published = time.strptime(published, '%Y-%m-%dT%H:%M:%S')
            new_post['published'] = datetime(*published[:6])
            # store id > title, created_time > published, message > abstract

            abstract = obj['message'].replace('\n', '')
            new_post['abstract'] = " ".join(abstract.strip().split())
            new_post['type_of'] = 'fb'

            w = orm_new_webresource(new_post)

            print "fb post stored"