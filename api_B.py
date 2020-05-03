from flask import render_template, request, redirect, url_for, jsonify

from SRC.config_params import PORT
from SRC.app import app
from SRC.mongo import *
from SRC.helpers.handle_errors import errorHandler, APIError
from SRC.recommender import GetRecommendation, GetjsonSingers
from SRC.sentiment import sentimentAnalysisGenre


# RUNNING APP
@app.route("/")
def wellcome():
    return render_template('home.html')


# ADD NEW SINGER/GENRE
@app.route("/create",methods=["GET","POST"])
@errorHandler
def CreateNew():
    if request.method=="POST":

        category = request.form.get("category")
        name=request.form.get("name")
        lista = GetListWithQuery(category, name) # check if name exists
        if lista:
            raise APIError(f"{name} already exists.")

        response = AddNew(category, name)
        return render_template('response.html', value=response)
    else:
        return render_template('createform.html')


# RECOMMEND SINGER 
@app.route("/recommend",methods=["GET","POST"])
@errorHandler
def RecommendMe():
    if request.method=="POST":

        name=request.form.get("name")      
        if CheckInfoAvailable ("singer.name", name):
            return jsonify(GetjsonSingers(name))

        raise APIError(f"{name} is not in the database or has no lyrics.")
    else:
        return render_template('generalform.html', 
                url ="/recommend", title="Find singers similars to:", category="Artist:")


# ADD LYRICS TO AN ARTIST
@app.route("/addlyrics",methods=["GET","POST"])
@errorHandler
def NewGenreWithPeople():
    if request.method=="POST":               
        
        name=request.form.get("name")
        lista = GetListWithQuery("singer", name) # Check name value       
        if lista:   
            lyrics = request.form.get("lyrics")                    
            response = AddLyrics(name, lyrics)
            return render_template('response.html', value=response)

        raise APIError(f"{name} is not in the database yet, why don't you create it?")
    else:
        return render_template('addlyricsform.html')


# SEE THE LYRICS OF A GENRE
@app.route("/seelyrics",methods=["GET","POST"])
@errorHandler
def ShowLyrics():
    if request.method=="POST":   

        name=request.form.get("name")        
        lista = GetListWithQuery("genre", name)  # Check genre name      
        if lista:  
            return jsonify(GetjsonLyrics(name))

        raise APIError(f"genre {name} is not in the database yet or has no lyrics")
    else:
        return render_template('generalform.html', 
                url ="/seelyrics", title="Enter a genre to see its lyrics", category="Genre:")



# SENTIMENT OF A GENRE
@app.route("/sentiment",methods=["GET","POST"])
@errorHandler
def SentimentGenre():
    if request.method=="POST":   

        name=request.form.get("name")              
        if CheckInfoAvailable ("genre", name):  
            response = sentimentAnalysisGenre(name)
            return jsonify(sentimentAnalysisGenre(name)) 
            #render_template('sentiment.html', 
                   # neg=response["neg"], neu=response["neu"], pos=response["pos"], comp=response["compound"])

        raise APIError(f"Genre {name} is not in the database yet or has no lyrics")
    else:
        return render_template('generalform.html', 
                url ="/sentiment", title="Enter a genre to see its sentiment", category="Genre:")



# ASSIGN ANOTHER GENRE TO A SINGER
@app.route("/assigngenre",methods=["GET","POST"])
@errorHandler
def AssignGenre():
    if request.method=="POST":   

        name=request.form.get("name")  
        genre=request.form.get("genre")   
        lista_1 = GetListWithQuery("singer", name)  # Check singer name  
        lista_2 = GetListWithQuery("genre", genre)  # Check genre name               
        if lista_1:
            if lista_2:
                response = ChangeGenre(genre, name)
                return render_template('response.html', value=response)
            raise APIError(f"{genre} is not in the database yet")

        raise APIError(f"{name} is not in the database yet")
    else:
        return render_template('assignform.html')



if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = PORT, debug=True) # Runs the app on a local development server
                                                       # "0.0.0.0": host available externally.

                                                  