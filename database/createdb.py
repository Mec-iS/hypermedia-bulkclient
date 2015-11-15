"""
Script to run to create the database' tables
"""
from datetime import datetime
from time import localtime

__author__ = 'Lorenzo'

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class WebResource(Base):
    __tablename__ = 'webresource'

    type_of_resource = ('feed', 'tweet', 'media', 'link', 'pdf', 'paper', 'fb', 'movie')

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String(250), nullable=False)
    in_graph = Column('in_graph', Boolean, nullable=False, default=False)
    url = Column('url', String(2083), nullable=False, unique=True)
    abstract = Column('abstract', Text())
    stored = Column('stored', DateTime(timezone=True), default=datetime(*localtime()[:6]))
    published = Column('published', DateTime(timezone=True))
    type_of = Column('type_of', String(15), nullable=False)
    parent_id = Column('parent_id', Integer, ForeignKey('webresource.id'), nullable=True)

    # http://stackoverflow.com/a/6264027/2536357
    # http://techspot.zzzeek.org/2011/01/14/the-enum-recipe/

    @property
    def serialize(self):
        # "Returns object data in easily serializable format"
        return {
            'id': self.id,
            'title': self.title,
            'type_of': self.type_of,
            'url': self.url
        }


class Indexer(Base):
    __tablename__ = 'indexer'

    id = Column(Integer, primary_key=True)
    webresource_id = Column(Integer, ForeignKey('webresource.id'))
    keyword = Column(String(101), nullable=False)
    webresource = relationship(WebResource)

    @property
    def serialize(self):
        # "Returns object data in easily serializable format"
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'description': self.description,
            'user_id': self.user_id,
        }

Index('idx_webres_url_id', WebResource.url, WebResource.id)
Index('idx_webres_type_of_published', WebResource.type_of, WebResource.stored)
Index('idx_webres_stored', WebResource.stored.desc())
Index('idx_webres_published', WebResource.published.desc())
Index('idx_webres_parent_id', WebResource.parent_id)


from config.secret import database_uri
engine = create_engine(database_uri)
Base.metadata.create_all(engine)

# Models' collections:
# Ship.__table__.columns will provide you with columns information
# Ship.__table__.foreign_keys will list foreign keys
# Ship.__table__.constraints, Ship.__table__.indexes
