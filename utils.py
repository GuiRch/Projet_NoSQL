#%%
import json
import sqlite3
from pymongo import MongoClient

#%%
def jsonToDict(JSONfile):
    with open(JSONfile) as json_data:
        data_dict = json.load(json_data)
    return(data_dict)

#print(jsonToDict('data.json'))

data = open("jeuDeDonnees_1.log", "r")
#print(data.read())

#%%
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def sqlToDict(database = 'database.db'):
    conn = sqlite3.connect(database)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute('select * from dataset')

    result = c.fetchall()
    return result

#print(type(sqlToDict()[0]))

#%%
def save_sql(dict):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    for line in range(len(dict)):
        id = jsonToDict('data.json')[line].get("id")
        event_type = jsonToDict('data.json')[line].get("event-type")
        occuredON = jsonToDict('data.json')[line].get("occuredON")
        version = jsonToDict('data.json')[line].get("version")
        graph_id = jsonToDict('data.json')[line].get("graph-id")
        nature = jsonToDict('data.json')[line].get("nature")
        object_name = jsonToDict('data.json')[line].get("object-name")
        path = jsonToDict('data.json')[line].get("path")

        data = (id, event_type, occuredON, version, graph_id, nature, object_name, path)
        cur.executemany(" INSERT INTO dataset (id, event_type, occuredON, version, graph_id, nature, object_name, path) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?) ", (data,))
        # the secure way to enter the variable
    conn.commit()
    conn.close()   

#save_sql(jsonToDict('data.json'))

def connectMongo(database,collection):
    try :
        client = MongoClient('localhost', 27017)
        db = client[database]
        collection = db[collection]
        return("connecté !")
    except ValueError:
        return("oups")


