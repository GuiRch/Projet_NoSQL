#%% 
import sqlite3
import json
from pymongo import MongoClient
from utils import jsonToDict
from utils import sqlToDict
from utils import connectMongo

#connectMongo('database','collection')

myclient = MongoClient("mongodb://localhost:27017/")

try:
    mydb = myclient["mydatabase"]
    print("database have been created !")
except:
    print("échec")

print(myclient.list_database_names())

dblist = myclient.list_database_names()

if "mydatabase" in dblist:
    print("The database exists.")
else:
    print("The database doesn't exist yet.") 



# # Build a basic dictionary
# d = {'website': 'www.carrefax.com', 'author': 'Daniel Hoadley', 'colour': 'purple'}

# # Insert the dictionary into Mongo
# collection.insert_one(d)


#%%

#client = MongoClient("mongodb+srv://<GuiRch>:<emAXxlWXgiqz3yvt>@cluster0.vwybs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#db = client.test
