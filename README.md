# Projet_NoSQL

## Installation
``pip install sqlite3``
Il faut également installer l'extension Sqlite sur Visual studio code ou utiliser un logiciel tiers pour visualiser comme DB Browser pour visualiser la base de donnée.

Sur VS Code : 
``ctrl`` ``shift`` ``P`` puis ```SQLite: Open Database`` dans la palette de commandes.

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
