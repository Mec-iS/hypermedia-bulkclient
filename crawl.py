import urllib
from bs4 import BeautifulSoup
from unidecode import unidecode

__author__ = 'Lorenzo'

from urllib import FancyURLopener

class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

results = []


def crawl_video_urls(url='http://documentaryheaven.com/category/space/'):
    myopener = MyOpener()
    page = myopener.open(url)
    page = page.read()

    html = BeautifulSoup(page, "lxml")

    # find all class=post
    posts = html.find_all('div', class_="post")

    # for each class=post:
    for p in posts:
        obj = {}
        #class=post-title --> a (href, string)
        title = p.find('h2').find('a')
        obj['url'] = title['href']
        obj['title'] = unidecode(title.string)
        abstract = p.find('div', class_='browse-description').find('p')
        obj['abstract'] = unidecode(abstract.string).replace('\n', '').replace('\r\r', ' ').strip()
        #class=browse-description --> p (string)

        results.append(obj)
    # next page: class=next --> (href)
    next_page = html.find('a', class_="next page-numbers")

    if not next_page:
        return None
    print results
    print next_page['href']

    return crawl_video_urls(url=next_page['href'])

crawl_video_urls()

