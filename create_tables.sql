
/* {u'in_graph': False, u'uuid': 5138567592411136L, u'title': u'TeleCommunication Systems', u'url': u'http://www.tmcnet.com/usubmit/2015/03/16/8159830.htm', u'abstract': u"...capable of tracking these satellite systems. * Future Department of Defense (DoD) reconnaissance applications...", u'keywords_url': u'http://localhost:8080/articles/v04/?url=http://www.tmcnet.com/usubmit/2015/03/16/8159830.htm', u'stored': u'2015-10-02T13:34:19', u'published': u'2015-03-16T11:59:47', u'type_of': u'feed'} */
/* length of a url field: http://stackoverflow.com/a/219664/2536357 */
CREATE TABLE webresource (
   uuid INTEGER CONSTRAINT webresource_uuid PRIMARY KEY,
   title VARCHAR(500),
   in_graph BOOLEAN NOT NULL DEFAULT FALSE,
   url VARCHAR (2083) NOT NULL UNIQUE,
   abstract TEXT,
   store TIMESTAMP,
   published TIMESTAMP,
   type_of VARCHAR(15)


);


/* {u'uuid': 4549229359923200L, u'keyword': u'reactor radiation safety measures (space applications)'} */
CREATE TABLE indexer (
   pk_id SERIAL PRIMARY KEY,
   resource_uuid INTEGER NOT NULL,
   keyword VARCHAR(101) NOT NULL
);