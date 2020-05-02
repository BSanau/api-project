from flask import render_template, request, redirect, url_for

from SRC.config_params import PORT
from SRC.app import app
from SRC.mongo import AddNew, GetListWithQuery
from SRC.helpers.handle_errors import errorHandler, APIError
from SRC.recommender import GetRecommendation


# RUNNING APP
@app.route("/")
def wellcome():
    return render_template('home.html')

# ADD NEW SINGER/GENRE
@app.route("/create",methods=["GET","POST"])
@errorHandler
def CreateNew():
    if request.method=="POST":
        # Check category value
        category=request.form.get("category")
        if category not in ["genre", "singer"]:
            raise APIError(f"{category} not in the database. Enter genre or singer.")

        # Check name value
        name=request.form.get("name")
        lista = GetListWithQuery(category, name)
        if lista:
            raise APIError(f"{name} already exists.")

        response = AddNew(category, name)
        return response
    else:
        return '''<form action="/create" method="POST">
                <label>Category:</label>
                <input type="text" name="category"/>
                <label>Name:</label>
                <input type="text" name="name"/><br/><br/>
                <input type="submit"/>
                </form>'''


# RECOMMEND SINGER TO ANOTHER SINGER
@app.route("/recommend",methods=["GET","POST"])
@errorHandler
def RecommendMe():
    if request.method=="POST":
        # Check name value
        name=request.form.get("name")
        lista = GetListWithQuery("singer", name)
        if lista:
            return GetRecommendation(name)#f"You wrote {name}"
        raise APIError(f"{name} not in the database or has no lyrics.")
    else:
        return '''<form action="/recommend" method="POST">
                <h1>Find singers similars to:</h1>
                <label>Name:</label>
                <input type="text" name="name"/><br/><br/>
                <input type="submit" value="Make recommendation"/>
                </form>'''


# ADD LYRICS TO AN ARTIST
@app.route("/addlyrics",methods=["GET","POST"])
@errorHandler
def NewGenreWithPeople():
    if request.method=="POST":               
        # Check name value
        name=request.form.get("name")
        lista = GetListWithQuery("singer", name)
        if lista:
            lyrics = request.form.get("lyrics")
            return f"You added lyrics to {name}"
        raise APIError(f"{name} is not in the database yet, why don't you create it?")
    else:
        return '''<form action="/addlyrics" method="POST">
                <h1>Add some lyrics</h1>
                <label>Artist:</label>
                <input type="text" name="name"/><br/><br/>
                <label>Lyrics:</label>
                <input type="text" lyrics="lyrics" size="50"/><br/><br/>
                <input type="submit" value="Add Lyrics"/>
                </form>'''
"""
## CREATE NEW SINGER/GENRE
@app.route("/<category>/create", methods = ["GET", "POST"])
@errorHandler
def AddNewCategory (category):
    if request.method == "GET":
        return render_template('paramspage.html')
    elif request.method == "POST":
        name = request.form["nm"]
        response = AddNew(category, name)
        return f"Inserted"
        #render_template('resultpage.html', response = response)
    #if category not in ["genre", "singer"]:
    #    raise APIError(f"{category} not in the database. Enter genre or singer.")
    #name = request.args["name"] #BORRAR
    #return AddNew(category, name) #BORRAR
    #return f"Add new {category}: {name}"
# En el navegador: localhost:3500/singer/create?name=Lola 
"""
"""
@app.route("/suma",methods=["GET","POST"])
def sumar():
    if request.method=="POST":
        num1=request.form.get("num1")
        num2=request.form.get("num2")
        return "<h1>El resultado de la suma es {}</h1>".format(str(int(num1)+int(num2)))
    else:
        return '''<form action="/suma" method="POST">
                <label>N1:</label>
                <input type="text" name="num1"/>
                <label>N2:</label>
                <input type="text" name="num2"/><br/><br/>
                <input type="submit"/>
                </form>'''
"""

# ARTISTS PAGE


"""
# TEST
@app.route("/test", methods = ["GET", "POST"])
def test():
    if request.method == "GET":
        return render_template('test.html')
    elif request.method == "POST":
        response = request.form["nm"]
        return f"You wrote {response}"
        #return redirect(url_for("beafunc", var="guapa"))

@app.route("/bea")
def beafunc(var):
    return f"Bea {var}"
"""

"""
# FINDING SINGER/GENRE
@app.route("/<category>/<name>", methods = ["GET", "POST"])
@errorHandler
def ShowData(category, name):
    if category not in ["genre", "singer"]:
        raise APIError(f"{category} not in the database. Enter genre or singer.")
    lista = GetListWithQuery(category, name)
    if lista:
        print(f"{category} tiene lista")
        return GetData (lista, category, name)
    raise APIError(f"{category}: {name} not in the database")


## CREATE NEW SINGER/GENRE
@app.route("/<category>/create", methods = ["GET", "POST"])
@errorHandler
def AddNewCategory (category):   
    if category not in ["genre", "singer"]:
        raise APIError(f"{category} not in the database. Enter genre or singer.")
    name = request.args["name"]
    return AddNew(category, name)
    #return f"Add new {category}: {name}"
# En el navegador: localhost:3500/singer/create?name=Lola 
"""

## ADD LYRICS
#@app.route("/singer/addlyrics", methods = ["GET", "POST"])


# SHOW ALL THE LYRICS FROM A GENRE/SINGER
#@app.route("/<category>/<name>/list", methods = ["GET", "POST"])


# ANALYZE THE SENTIMENT OF A GENRE/SINGER
#@app.route("/<category>/<name>/sentiment", methods = ["GET", "POST"])


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = PORT, debug=True) # Runs the app on a local development server
                                                       # "0.0.0.0": host available externally.

                                                  