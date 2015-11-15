__author__ = 'Lorenzo'

ENV = {'offline': {'_SERVICE': 'http://localhost:8080',
                   '_DEBUG': True},
       'online': {'_SERVICE': 'http://hypermedia.projectchronos.eu',
                   '_DEBUG': True}}


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from secret import database_uri
engine = create_engine(database_uri, pool_size=20, max_overflow=0)
DBSession = scoped_session(sessionmaker(bind=engine))


