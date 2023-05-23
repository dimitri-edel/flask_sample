from flask import render_template
from flask_sample_app import app


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/careers")
def careers():
    return render_template("careers.html")