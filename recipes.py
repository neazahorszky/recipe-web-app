from flask import session
from sqlalchemy import text
from db import db

def new_recipe(name, ingredients, instructions):
    creator = session["user_id"]
    sql = text("INSERT INTO recipes (name, user_id, ingredients, instructions) VALUES (:name, :user_id, :ingredients, :instructions) RETURNING id")
    obj = db.session.execute(sql, {"name":name, "user_id":creator, "ingredients": ingredients, "instructions": instructions})
    for i in obj:
        id = i[0]
    db.session.commit()
    return id
    

def get_list_recipes():
    sql = text("SELECT id, name FROM recipes")
    return db.session.execute(sql).fetchall()

def get_recipe(recipe_id):
    sql = text('''SELECT r.name, u.name, r.ingredients, r.instructions 
                FROM recipes r, users u 
                WHERE r.id = :id AND u.id = r.user_id''')

    return db.session.execute(sql, {"id" : recipe_id}).fetchone()
