from flask import render_template, request, redirect
from app import app
import users
import recipes
import reviews
import categories

@app.route("/", methods=["get","post"])
def index():
    browse_categories = False
    if request.method == "POST":
        by_category = request.form["browse_categories"]
        if by_category == "True":
            browse_categories = True
        else:
            browse_categories = False
        return render_template("index.html", recipes=recipes.get_list_recipes(), browse_categories=browse_categories, categories=categories.get_categories())

    return render_template("index.html", recipes=recipes.get_list_recipes(), browse_categories=browse_categories, categories=categories.get_categories())

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

@app.route("/category/<int:category_id>")
def category(category_id):
    category_name, category_description = categories.get_category(category_id)
    recipes_in_category = categories.get_recipes_category(category_id)
    return render_template("category.html", category_id=category_id, category_name=category_name, category_description=category_description, recipes=recipes_in_category)

@app.route("/addcategory", methods=["get","post"])
def add_category():
    if request.method == "GET":
        return render_template("addcategory.html")
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        category_id = categories.add_category(name, description)
        if category_id:
            return redirect("/category/" + str(category_id))
        return render_template("error.html", message="Category could not be added")

@app.route("/addtocategory/<int:category_id>", methods=["get","post"])
def addtocategory(category_id):
    if request.method == "GET":
        category = categories.get_category(category_id)
        return render_template("addtocategory.html", category_id=category_id, category=category, recipes=recipes.get_list_recipes())
    if request.method == "POST":
        recipe_list = request.form.getlist("recipe")
        added = categories.add_to_category(category_id, recipe_list)
        if added:
            return redirect("/category/" + str(category_id))
        return render_template("error.html", message="Recipe(s) could not be added to category")

@app.route("/search")
def search_result():
    query = request.args["query"]
    matching_recipes = recipes.search_recipes(query)
    return render_template("search.html", query=query, recipes=matching_recipes)