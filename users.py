from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from sqlalchemy import text
from db import db

def login(username, password):
    sql = text("SELECT password, id, name FROM users WHERE name=:name")
    result = db.session.execute(sql, {"name":username}).fetchone()
    if not result:
        return False
    else:
        if check_password_hash(result[0], password):
            session["user_id"] = result[1]
            session["username"] = result[2]
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["username"]

def signup(username, password, role):
    try:
        hash_value = generate_password_hash(password)
        sql = text("INSERT INTO users (name, password, role) VALUES (:name, :password, :role)")
        db.session.execute(sql, {"name":username, "password":hash_value, "role":role})
        db.session.commit()

    except:
        return False

    return login(username, password)

