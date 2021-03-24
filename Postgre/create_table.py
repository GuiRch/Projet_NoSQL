import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    command = (
        """
        CREATE TABLE data (
            id VARCHAR(256) PRIMARY KEY,
            event_type VARCHAR(256) NOT NULL,
            occuredOn TIMESTAMP,
            version INT,
            graph_id VARCHAR(256),
            nature VARCHAR(256),
            object_name VARCHAR(256),
            path SET(RECEIVED, VERIFIED,
PROCESSED, REJECTED, REMEDIED, PROCESSED, CONSUMED, TO_BE_PURGED, PURGED)
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()