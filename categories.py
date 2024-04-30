from flask import session
from sqlalchemy import text
from db import db

def add_category(name, description):
    try:
        sql = text("INSERT INTO categories (name, description) VALUES (:name, :description) RETURNING id")
        result = db.session.execute(sql, {"name":name, "description":description})
        for r in result:
            id = r[0]
        db.session.commit()
        return id
    except:
        return False

def add_to_category(category_id, recipe_id_list):
    try:
        sql = text("INSERT INTO recipes_categorized (category_id, recipe_id) VALUES (:category_id, :recipe_id)")
        for recipe_id in recipe_id_list:
            result = db.session.execute(sql, {"category_id": category_id, "recipe_id": recipe_id})
        db.session.commit()
        return True
    except:
        return False
    
def get_categories():
    sql = text("SELECT id, name FROM categories")
    return db.session.execute(sql).fetchall()

def get_category(category_id):
    sql = text("SELECT name, description FROM categories WHERE id = :category_id")
    return db.session.execute(sql, {"category_id": category_id}).fetchone()

def get_recipes_category(category_id):
    sql = text("SELECT r.id, r.name FROM recipes r JOIN recipes_categorized c ON r.id = c.recipe_id WHERE category_id=:category_id")
    return db.session.execute(sql, {"category_id": category_id}).fetchall()