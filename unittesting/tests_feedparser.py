import feedparser

__author__ = 'Lorenzo'


f = feedparser.parse('http://www.esa.int/rssfeed/TopMultimedia')

print isinstance(f, dict) and 'entries' in f

print f