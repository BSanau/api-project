import pandas as pd

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pymongo import MongoClient
from scipy.spatial.distance import pdist, squareform

from SRC.config_params import DBURL, collName
from SRC.mongo import ConnectToMongoDB, GetListWithQuery


def GetDFfromCursor():
    cursor, db = ConnectToMongoDB()
    lista = list(cursor.find({}, {"_id":0, "singer.name":1, "singer.lyrics":1})) # find all
    df_data = pd.DataFrame(lista) # convert to df
    df_data = df_data.dropna(axis=0) # drop rows without singer entry
    return df_data


def GetSentiments():
    df = GetDFfromCursor()
    
    sia = SentimentIntensityAnalyzer() 

    dicc = {}                                # create a dictionary to store the values generated
    for i in df.index:                       # with the Sentiment Analyzer
        row = df[["singer"]].loc[i][0]
        for e in row:
            if "lyrics" in e.keys():
                value = " ".join(e["lyrics"])
                res = sia.polarity_scores(value)
                dicc[e["name"]] = {
                    "name": e["name"],
                    "neg": res["neg"], 
                    "neu": res["neu"], 
                    "pos": res["pos"], 
                    "compound": res["compound"]}

    singers_df = pd.DataFrame(dicc.values()).set_index("name") # convert dict into df
    return singers_df


def GetRecommendation(name):
    df = GetSentiments()
    distances = pd.DataFrame(1/(1 + squareform(pdist(df, 'euclidean'))), # matrix of euclidean distances
                         index=df.index, columns=df.index)
    top3 = distances[name].sort_values(ascending=False)[1:4].index #find top 3 most similar
    return top3


def GetjsonSingers(name):
    top3 = GetRecommendation(name)
    jsonfile = {}
    for singer in top3:
        lista = GetListWithQuery("singer", singer) 
        lyrics = [e["lyrics"] for e in lista[0]["singer"] if e["name"]==singer] # get lyrics from a singer
        jsonfile[singer] = lyrics[0]
    return jsonfile