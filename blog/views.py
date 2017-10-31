from flask import Flask, request, session, redirect, url_for, render_template, flash
from .models import User


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User(username)

        if not user.register(password):
            flash("A user with that username already exists.")
        else:
            flash("Successfully registered.")
            return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User(username)

        if not user.verify_password(password):
            flash("Invalid Login.")
        else:
            flash("Succesfully logged in.")
            session["username"] = user.username
            return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/add_post", methods=["Post"])
def add_post():
    title = request.form["title"]
    tags = request.form["tags"]
    text = request.form["text"]

    user = User(session["useranem"])

    if not title or not tags or not text:
        flash("You must give your post a title,tags, and a text body.")
    else:
        user.add_post(title,tags,text)

    return redirect(url_for("index"))


@app.route("/like_post/<post_id>")
def like_post(post_id):
    return "TODO"


@app.route("/profile/<username>")
def profile(username):
    return "TODO"


@app.route("/logout")
def logout():
    return "TODO"