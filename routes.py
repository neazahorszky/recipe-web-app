from flask import render_template, request, redirect
from app import app
import users
import recipes
import reviews

@app.route("/")
def index():
    return render_template("index.html", recipes=recipes.get_list_recipes())

@app.route("/login", methods=["get","post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Username or password incorrect")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/signup", methods=["get","post"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Passwords did not match")
        role = request.form["role"]
        if role != "1" and role != "2":
            return render_template("error.html", message="Unkonwn user role")
        if users.signup(username, password1, role):
            return redirect("/")
        else:
            return render_template("error.html", message="Sign-up unsuccessful")

        return redirect("/")

@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    recipe_data = recipes.get_recipe(recipe_id)
    
    if recipe_data:
        name, creator, ingredients, instructions = recipe_data[0], recipe_data[1], recipe_data[2], recipe_data[3]
        ingredients_list = ingredients.split(",")
        reviews_list = reviews.get_reviews(recipe_id)
        return render_template("recipe.html", name=name, creator=creator, ingredients=ingredients_list, instructions=instructions, \
            recipe_id=recipe_id, reviews_list=reviews_list)
    else:
        return render_template("error.html", message="Recipe does not exist")

@app.route("/addrecipe", methods=["get","post"])
def addrecipe():
    if request.method == "GET":
        return render_template("addrecipe.html")
    if request.method == "POST":
        name = request.form["name"]
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]
        recipe_id = recipes.new_recipe(name, ingredients, instructions)
        if recipe_id is not None:
            return redirect("/recipe/" + str(recipe_id))
        else:
            return render_template("error.html", message="Recipe could not be added")

@app.route("/review/<int:recipe_id>", methods=["get", "post"])
def review(recipe_id):
    recipe_data = recipes.get_recipe(recipe_id)
    recipe_name = recipe_data[0]
    if request.method == "GET":
        return render_template("review.html", recipe_name=recipe_name, recipe_id=recipe_id)
    if request.method == "POST":
        rating = request.form["rating"]
        comment = request.form["comment"]
        create_review = reviews.new_review(recipe_id, rating, comment)
        if create_review:
            return redirect("/recipe/" + str(recipe_id))
        else:
            return render_template("error.html", message="Review could not be added")