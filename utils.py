#%%
import json
import sqlite3
from pymongo import MongoClient

#%%
def jsonToDict(JSONfile='data.json'):
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
def save_sql(dict=jsonToDict('data.json')):
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

def insertMongo(liste=jsonToDict('data.json')):
    # Connect to Mongo
    client = MongoClient(port=27017)
    db = client.data
    try:
        for elem in liste:
            result = db.element.insert_one(elem)
        return("elements stored succesfuly")
    except:
        return("an error occured")

#insertMongo()
def parseString(string="[RECEIVED, VERIFIED, PROCESSED, CONSUMED]"):
    string = string[1:]
    string = string[:-1]

    string = string.split(', ')
    return(string)

#parseString()


# def replaceMongo(database='data',collection='element'):
#     myclient = MongoClient("mongodb://localhost:27017/")
#     mydb = myclient[database]
#     mycol = mydb[collection]

