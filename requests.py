import redis
import json

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
        #on enlève les dixièmes de seconde de la date
        r.hset( id, "occurredOn", x["occurredOn"].split('.')[0])
        r.hset( id, "version", x["version"])
        r.hset( id, "graph-id", x["graph-id"])
        r.hset( id, "nature", x["nature"])
        r.hset( id, "object-name", x["object-name"])
        r.hset( id, "path", x["path"])

    return None


jsonToRedis()


#Récupérer le cycle de vie parcouru (la liste des status d’un objet donné)
def statusObject(id):
    s = r.hget(id, "path")
    st = s.decode()
    st = st[1:-1]
    status = [x.strip() for x in st.split(',')]
    return status


#statusObject("db2316d6-6b30-4c30-8c79-586ca0c06c21")


#Compter le nombre d’objets par status
def countObjStatus(status):
    counter = 0
    for k in r.keys():
        key = k.decode()
        allStatus = statusObject(key)
        if status in allStatus:
            counter +=1
    return counter

"""
print("nombre de RECEIVED : ", countObjStatus('RECEIVED'))
print("nombre de VERIFIED : ", countObjStatus('VERIFIED'))
print("nombre de PROCESSED : ", countObjStatus('PROCESSED'))
print("nombre de CONSUMED : ", countObjStatus('CONSUMED'))
print("nombre de REJECTED : ", countObjStatus('REJECTED'))
print("nombre de REMEDIED : ", countObjStatus('REMEDIED'))
print("nombre de TO_BE_PURGED : ", countObjStatus('TO_BE_PURGED'))
print("nombre de PURGED : ", countObjStatus('PURGED'))
"""



#Compter le nombre d’objets respectant l’intégrité du graphe du cycle de vie

def completeCycle():
    counter = 0
    cyclePart = '[RECEIVED, VERIFIED, PROCESSED, CONSUMED]'
    purgePart = '[TO_BE_PURGED, PURGED]'

    #associe chaque id à son object-name et récupère une liste de tous les object-name possible (sans répétition)
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



