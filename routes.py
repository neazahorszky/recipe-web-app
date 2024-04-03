from flask import render_template, request, redirect
from app import app
import users

@app.route("/")
def index():
    return render_template("index.html")

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