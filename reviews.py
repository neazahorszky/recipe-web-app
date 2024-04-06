from flask import session
from sqlalchemy import text
from db import db

def new_review(recipe_id, rating, comment):
    try: 
        creator_id = session["user_id"]
        sql = text("INSERT INTO reviews (user_id, recipe_id, rating, comment) VALUES (:user_id, :recipe_id, :rating, :comment)")
        db.session.execute(sql, {"user_id": creator_id, "recipe_id": recipe_id, "rating": rating, "comment":comment})
        db.session.commit()
        return True
    except:
        return False


def get_reviews(recipe_id):
    ...
