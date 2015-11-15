import psycopg2

__author__ = 'Lorenzo'


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=hypermedia user=chronos")


def store_webresource(resource):
    conn = connect()
    cur = conn.cursor()
    SQL = "INSERT INTO webresource(uuid, title, in_graph, url, abstract, store, published, type_of) " \
          "VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
    data = (
        resource['uuid'], resource['title'], resource['in_graph'], resource['url'],
        resource['abstract'], resource['store'], resource['published'], resource['type_of']
    )
    cur.execute(SQL, data)
    conn.commit()

    cur.close()
    conn.close()

    return True


def store_indexer(indexed):
    conn = connect()
    cur = conn.cursor()
    SQL = "INSERT INTO indexer(resource_uuid, keyword) " \
          "VALUES(%s, %s);"
    data = (indexed['uuid'], indexed['keyword'])
    cur.execute(SQL, data)
    conn.commit()

    cur.close()
    conn.close()

    return True