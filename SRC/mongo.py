from pymongo import MongoClient

from SRC.config_params import DBURL, collName


def ConnectToMongoDB(): # No need to enter DBURL and collName, they are defined as env variables
    client = MongoClient(DBURL)
    db = client.get_database() # Gets all the databases from the client
    cursor = eval(f"db.{collName}") # Selecting the collection set
    return cursor, db


def GetListWithQuery(category, name): # category could be either singer or genre        
    cursor, db = ConnectToMongoDB()
    if category == "singer":          # query in case singer
        myquery = {"singer.name": name}
    elif category == "genre":         # query in case genre
        myquery = {"genre": name}
    fields = {"_id":0, "genre":1, "singer":1}
    lista = list(cursor.find(myquery, fields))
    return lista


def AddNew(category, name):
    cursor, db = ConnectToMongoDB()    
    if category == "genre": # if name is genre, insert as genre and return a message
        cursor.insert_one({"genre": f"{name}"}, {"_id":1})
        return f"{name} added as {category}."
    if category == "singer": # if name is singer, insert as singer and return a message
        cursor.update_one(
            { "genre": "uncategorized" },
            { "$push": {"singer": {"name": f"{name}"}} }
        )
        return f"{name} added as {category}"


def CheckInfoAvailable (category, name):                                       
    cursor, db = ConnectToMongoDB()
    lista = list(cursor.find({category: name}, {"_id":0, "singer":1}))
    if lista and lista[0]: # aquí me cargo los que no existen y los genre sin cantantes
        for e in lista[0]["singer"]: 
            if "lyrics" in e.keys(): # aquí dejo fuera los cantantes sin canción
                if category == "genre": return True # genre exists
                if category == "singer.name" and e["name"]==name: return True # singer exists
    return False


def AddLyrics(name, lyrics):
    cursor, db = ConnectToMongoDB() # Necesitamos sacar esto para tener el db
    lista = list(cursor.find({"singer.name": name}, {"_id":0, "genre":1}))
    genre = lista[0]["genre"]

    db.lyrics.update_one(  # Add lyrics to singer.lyrics entry in the genre found
        { "genre": genre , "singer.name": name},
        { "$push": {"singer.$.lyrics": lyrics}}
    )   
    return f"Lyrics added to {name}" 


def GetjsonLyrics(name): 
    lista = GetListWithQuery("genre", name)  
    lyricsjson = {e["name"]:e["lyrics"] for e in lista[0]["singer"]} # Get json
    return lyricsjson


def ChangeGenre(name_genre, name_singer):
    cursor, db = ConnectToMongoDB() # Necesitamos sacar esto para tener el db

    # Check info from name and save it into "info"
    lista = list(cursor.find({"singer.name": name_singer}, {"_id":0, "genre":1, "singer":1}))
    old_genre = lista[0]["genre"]
    info = [e for e in lista[0]["singer"] if e["name"]==name_singer]

    # Add info to new genre
    db.lyrics.update_one(
            { "genre": name_genre},
            { "$push": {"singer": info[0]}}
        )

    # Delete info from old genre
    #db.lyrics.update_one(
    #{ "genre": old_genre },
    #{ "$pull": {"singer": {"name": name}}}
    #)
      
    return f"Update genre for {name_singer}"