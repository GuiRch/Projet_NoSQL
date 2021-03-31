# Projet_NoSQL

## Installation
``pip install sqlite3``
Il faut également installer l'extension Sqlite sur Visual studio code ou utiliser un logiciel tiers pour visualiser comme DB Browser pour visualiser la base de donnée.

Sur VS Code : 
``ctrl`` ``shift`` ``P`` puis ``SQLite: Open Database`` dans la palette de commandes.

Pour la partie Redis, installez redis-py avec ``pip install redis``

## Gestion des données brut:

Dans un premier temps nous avons transformé le fichier jeuDeDonnees_1.log en data.json, étant donné qu'un ficher json est plus facilement manipulable.

    def jsonToDict(JSONfile):
        with open(JSONfile) as json_data:
            data_dict = json.load(json_data)
        return(data_dict)

Cette fonction nous permet ensuite de convertir ce fichier Json en un dictionnaire python.

## Création de la base de données SQL 

On utilise sqlite pour gèrer notre base de donnée. Ainsi, pour créer la base de donnée, on lance la commande :

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    req = "CREATE TABLE dataset( id string primary key, event_type TEXT, occuredOn DATETIME, version INT, graph_id TEXT, nature TEXT, object_name TEXT, path TEXT) "
    cur.execute(req)

    conn.commit()
    conn.close()

Commande qui se trouve dans le fichier ``create_table_sqlite.py``


## Base de données SQL

Pour enregistrer les données dans la base de données SQL, nous avons choisi d'utiliser sqlite. Sqlite et facile et assez rapide à prendre en main grâce à python. Pour enregistrer les données sur la base de données nous utilisons la fonction suivante :

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
  
Cette fonction ce trouve dans ``utils.py`` et peut être appellée en utilisant simplement save_sql(jsonToDict('NomDuFichier.json')).  

## Création de la base de données Mongo et projection des données

La création de la base de données ``data`` se fait dans la fonction qui va inserer les la liste des dictionnaires dans la base de donnée Mongo avec la fonction ``insertMongo`` dans le fichier ``utils.py``

Pour utiliser la fonction d'insertion dans la base de donnée Mongo, il faut au préalable lancer les codes suivant dans deux consoles séparés :

    cd c:\Integ
    cd mongodb-win32...
    bin\mongod --dbpath data

puis :

    cd c:\Integ
    cd mongodb-win32...
    bin\mongo

## Les requêtes MongoDB :

### Récupérer le cycle de vie parcouru (la liste des status d’un objet donné)

Pour cela il faut lancer la fonction ``findById`` :

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

par exemple : ``print(findByI("db2316d6-6b30-4c30-8c79-586ca0c06c21"))``

Il est également possible de récupèrer la liste des status d'un objet par son nom comme par exemple : ``print(findByName("File-25"))`` qui renvoie : ``[['File-25', '[TO_BE_PURGED, PURGED]'], ['File-25', '[RECEIVED, VERIFIED, PROCESSED, CONSUMED]'], ['File-25', '[RECEIVED, VERIFIED, PROCESSED, CONSUMED]'], ['File-25', '[RECEIVED, VERIFIED, PROCESSED, REJECTED, REMEDIED]']]`` grâce à la fonction :

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


### Compter le nombre d’objets par status 

Tout d'abord, on crée une fonction qui permet de retrouver tout les objets qui comporte le status souhaité, que l'on stocke par la suite dans une liste. Cette fonction est la fonction ``findStatus`` puis on compte le nombre d'élements de la liste retournée par la fonction ``findStatus``.

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

    def countStatus(status):
        return(len(findStatus(status)))

Pour avoir la liste de tout les objets par status, lancez le script suivant : 

        
    list_of_status = ['TO_BE_PURGED', 'PURGED', 'RECEIVED', 'VERIFIED', 'PROCESSED', 'REJECTED', 'REMEDIED','CONSUMED']

    for status in list_of_status:
        print(status, " : ", countStatus(status))
        

## Création de la base de données Redis

Dans une première console, lancer redis avec la commande
```
cd Integ/redis-6.2-rc1
redis-server
```

puis dans une autre console : 
```
redis-cli
```

Il est possible de vérifier si le serveur est bien lancé avec la commdande ``ping`` qui doit répondre "PONG".
Une fois cela fait, vous pouvez exécuter le code se trouvant dans *requests.py*
