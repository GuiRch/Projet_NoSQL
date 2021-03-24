#%%
import json
import sqlite3

#%%
def jsonToDict(JSONfile):
    with open(JSONfile) as json_data:
        data_dict = json.load(json_data)
    return(data_dict)

print(jsonToDict('data.json'))

data = open("jeuDeDonnees_1.log", "r")
print(data.read())
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

        data = (id, event_type, occuredON, version, graph_id, nature, object_name)
        cur.executemany(" INSERT INTO dataset (id, event_type, occuredON, version, graph_id, nature, object_name) VALUES ( ?, ?, ?, ?, ?, ?, ?) ", (data,))
        # the secure way to enter the variable
    conn.commit()
    conn.close()   

save_sql(jsonToDict('data.json'))


