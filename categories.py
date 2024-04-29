from flask import session
from sqlalchemy import text
from db import db

def get_categories():
    sql = text("SELECT id, name FROM categories")
    return db.session.execute(sql).fetchall()

def get_category(category_id):
    sql = text("SELECT name, description FROM categories")
    return db.session.execute(sql).fetchone()

def get_recipes_category(category_id):
    sql = text("SELECT r.id, r.name FROM recipes r JOIN recipes_categorized c ON r.id = c.recipe_id WHERE category_id=:category_id")
    return db.session.execute(sql, {"category_id": category_id}).fetchall()