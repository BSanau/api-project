from nltk.sentiment.vader import SentimentIntensityAnalyzer

from SRC.config_params import DBURL, collName
from SRC.mongo import ConnectToMongoDB

def sentimentAnalysisGenre (name):
    cursor, db = ConnectToMongoDB()
    myquery = {"genre": name}
    fields = {"_id":0, "singer.lyrics":1}
    lista = list(cursor.find(myquery, fields))
    genre_lyrics = []
    for lyrics_of_singer in lista[0]["singer"]:
        if "lyrics" in lyrics_of_singer.keys():
            for lyrics in lyrics_of_singer["lyrics"]:
                genre_lyrics.append(lyrics)
    genre_lyrics = ", ".join(genre_lyrics)
    sia = SentimentIntensityAnalyzer()
    res = sia.polarity_scores(genre_lyrics)
    return res