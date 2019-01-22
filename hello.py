from flask import Flask, render_template, url_for

import os
app = Flask(__name__)


# @app.route("/")
# def hello_world():
#     return render_template("home.html")

@app.route("/")
def images():
    images = os.listdir('static/Categories/Category_0')
    images = ['Categories/Category_0/' + file for file in images]
    print(images)
    return render_template('images.html',images=images)

@app.route("/animals")
def animals():
    return render_template('category.html',info="animals")

@app.route("/humans")
def humans():
    return render_template('category.html',info="humans")

@app.route("/nature")
def nature():
    return render_template('category.html',info="nature")

@app.route("/other")
def other():
    return render_template('category.html',info="other")

if __name__ == "__main__":
    app.run()
