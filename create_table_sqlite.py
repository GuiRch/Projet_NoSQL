import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

req = "CREATE TABLE dataset( id string primary key, event_type TEXT, occuredOn DATETIME, version INT, graph_id TEXT, nature TEXT, object_name TEXT, path TEXT) "
cur.execute(req)

conn.commit()
conn.close()

