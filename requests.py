import redis
import redis
import json
import time
import datetime
from datetime import datetime

r = redis.Redis(host='localhost', port=6379, db=0)


#démarre d'une database vide
def jsonToRedis(database = 'data.json'):
    with open(database) as f:
        data = json.load(f)

    index = 1
    for x in data :
        #cas où on ajoute le premier field
        id = x["id"]
        r.hset( id, "event-type", x["event-type"])
        r.hset( id, "occurredOn", x["occurredOn"])
        r.hset( id, "version", x["version"])
        r.hset( id, "graph-id", x["graph-id"])
        r.hset( id, "nature", x["nature"])
        r.hset( id, "object-name", x["object-name"])
        r.hset( id, "path", x["path"])

    return None

jsonToRedis()




#Récupérer le cycle de vie parcouru (la liste des status d’un objet donné)

def statusObject(obj):
    #associe chaque id à son object-name et récupère une liste de tous les object-name possibles (sans répétition)
    keyObject = {}
    objectNames = []
    for k in r.keys():
        key = k.decode()
        keyObject[key] = (r.hget(key, "object-name")).decode()
        objectNames.append((r.hget(key, "object-name")).decode())
    objectNames = list(dict.fromkeys(objectNames))

    #parcourt les object-name existant dans la base de données
    for elt in objectNames:
        if elt == obj:
            #récupère la liste des ids ayant le même object-name
            sameObject = [k for k,v in keyObject.items() if v == elt]
            objectPaths = []
            pathTimestamps = {}

            #récupère le path de chaque id pour un object et le stocke dans une liste
            for id in sameObject:

                #récupère la date et la transforme en timestamp
                timestamp = r.hget(id,"occurredOn").decode()
                timestamp = timestamp.replace('T',' ')
                dt_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
                millisec = dt_obj.timestamp() * 1000
                #stocke tous les timestamp dans un dictionnaire, associé à leur id
                pathTimestamps[id] = millisec

            #trie le dictionnaire dans l'ordre décroissant des timestamp (le plus grand est le plus vieux, donc est la première occurence de l'object)
            pathTimestamps = dict(sorted(pathTimestamps.items(), key=lambda item: item[1], reverse = True))
            for key in pathTimestamps:
                #objectPaths.append(r.hget(key,"path").decode())
                paths = r.hget(key,"path").decode()
                paths = paths[1:-1]
                path = [x.strip() for x in paths.split(',')]
                objectPaths.append(path)

    return objectPaths


#print(statusObject('File-32'))



#Compter le nombre d’objets par status
def countObjStatus(status):
    counter = 0
    keyObject = {}
    objectNames = []
    for k in r.keys():
        key = k.decode()
        keyObject[key] = (r.hget(key, "object-name")).decode()
        objectNames.append((r.hget(key, "object-name")).decode())
    objectNames = list(dict.fromkeys(objectNames))

    #parcourt tous les objets de la bdd
    for obj in objectNames:
        #récupère le cycle de vie de l'objet
        paths = statusObject(obj)
        present = False
        #regarde si le status est présent dans le cycle de l'objet
        for path in paths:
            if status in path:
                present = True
        #s'il est présent on incrémente le compteur
        if present == True:
            counter += 1
    return counter


"""
print("nombre d'objet ayant VERIFIED : ", countObjStatus('VERIFIED'))
print("nombre d'objet ayant PROCESSED : ", countObjStatus('PROCESSED'))
print("nombre d'objet ayant CONSUMED : ", countObjStatus('CONSUMED'))
print("nombre d'objet ayant REJECTED : ", countObjStatus('REJECTED'))
print("nombre d'objet ayant REMEDIED : ", countObjStatus('REMEDIED'))
print("nombre d'objet ayant TO_BE_PURGED : ", countObjStatus('TO_BE_PURGED'))
print("nombre d'objet ayant PURGED : ", countObjStatus('PURGED'))
"""


def countIt(status):
    status = countObjStatus(status)
    return NotImplemented





#Compter le nombre d’objets par status sur la dernière heure

"""
L'idée était de réutiliser la fonction countObjStatus() afin d'avoir accès aux objets ayant le status
demandé, en rajoutant une condition sur l'heure. Pour cela, nous allions récupérer l'heure d'occurence
du status et l'heure actuelle en timestamp, et vérifier si la différence entre les 2 étaient inférieure
à 1h.
"""
def countStatusHour(status):
    #timestamp de la date et heure actuelles
    now = time.time()
    return NotImplemented





#Compter le nombre d’objets respectant l’intégrité du graphe du cycle de vie

def completeCycle():
    counter = 0
    cyclePart = '[RECEIVED, VERIFIED, PROCESSED, CONSUMED]'
    purgePart = '[TO_BE_PURGED, PURGED]'

    #associe chaque id à son object-name et récupère une liste de tous les object-name possibles (sans répétition)
    keyObject = {}
    objectNames = []
    for k in r.keys():
        key = k.decode()
        keyObject[key] = (r.hget(key, "object-name")).decode()
        objectNames.append((r.hget(key, "object-name")).decode())
    objectNames = list(dict.fromkeys(objectNames))

    #parcourt les object-name existant dans la base de données
    for elt in objectNames:
        #récupère la liste des ids ayant le même object-name
        sameObject = [k for k,v in keyObject.items() if v == elt]
        objectPaths = []

        #récupère le path de chaque id pour un object et le stocke dans une liste
        for id in sameObject:
            objectPaths.append(r.hget(id,"path").decode())
            objectPaths = list(dict.fromkeys(objectPaths))

        #regarde si les paths d'un object contiennent bien le chemin requis pour respecter l'intégrité d'un cycle
        if (cyclePart in objectPaths) and (purgePart in objectPaths):
            counter += 1

    return counter


#print(completeCycle())


