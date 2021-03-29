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



#%% Compter le nombre d’objets par status 


