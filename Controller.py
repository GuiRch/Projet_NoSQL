#%% 
import sqlite3
import json
import pprint
from pymongo import MongoClient
from utils import jsonToDict
from utils import sqlToDict
from utils import insertMongo

#%%

#Trouver le cycle de vie parcouru (la liste des status d'un objet donné)
def findById( id, database='data', collection='element'):
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient[database]
    mycol = mydb[collection]

    myquery = { "id": id }
    mydoc = mycol.find(myquery)

    l = []
    for x in mydoc:
        l.append(x)

    return l[0]

print(findById("db2316d6-6b30-4c30-8c79-586ca0c06c21"))

#%%

def findByName( name, database='data', collection='element'):
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient[database]
    mycol = mydb[collection]

    myquery = { "object-name": name }
    mydoc = mycol.find(myquery)

    l = []
    for x in mydoc:
        l.append(x)
    
    list_status=[]
    for elem in l:
        list_status.append([elem.get("object-name"),elem.get("path")])

    return list_status

print(findByName("File-25"))


#%% Compter le nombre d’objets par status 

def findStatus(string, database='data', collection='element'):
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient[database]
    mycol = mydb[collection]

    # mycol.create_index("path")
    # myquery = ({"$text": {"$search": string}})
    myquery = {'path': {'$regex': string}}
    mydoc = mycol.find(myquery)

    l = []
    for x in mydoc:
        l.append(x)

    return(l)

#findStatus('RECEIVED')

def countStatus(status):
    return(len(findStatus(status)))

#countStatus('RECEIVED')

list_of_status = ['TO_BE_PURGED', 'PURGED', 'RECEIVED', 'VERIFIED', 'PROCESSED', 'REJECTED', 'REMEDIED','CONSUMED']

for status in list_of_status:
    print(status, " : ", countStatus(status))

#%%
life = []

def cycleOfLife(name,database = 'data', collection = 'element'):
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient[database]
    mycol = mydb[collection]

    life = findByName(name)

    cyclePart = '[RECEIVED, VERIFIED, PROCESSED, CONSUMED]'
    purgePart = '[TO_BE_PURGED, PURGED]'


