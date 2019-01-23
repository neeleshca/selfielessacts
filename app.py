from flask import Flask, render_template, url_for
from inspect import getsourcefile
from os.path import abspath

import os

app = Flask(__name__)

PATH = abspath(getsourcefile(lambda: 0)).rsplit("/", 1)[0]
# @app.route("/")
# def hello_world():
#     return render_template("home.html")


@app.route("/")
def images():
    # print("hello")
    # print("12 4",os.listdir('static'))

    # images = os.listdir('static/Categories/Category_0')
    images = os.listdir(PATH + "/static/Categories/Category_0")
    print(images)
    for i in images:
        print(i)
    images = ["Categories/Category_0/" + file for file in images]
    print(images)
    return render_template("images.html", images=images)


@app.route("/test1")
def fun1():
    print("ONSIDIE\n")
    return render_template("testl.html")


@app.route("/user/<username>")
def show_user_profile(username):
    # show the user profile for that user
    return "User %s" % username


@app.route("/animals")
def animals():

    images = os.listdir(PATH + "/static/Categories/animals")
    images = ["Categories/animals/" + file for file in images]
    return render_template("category.html", info="animals", images=images)

    # return render_template('category.html',info="animals")


@app.route("/humans")
def humans():

    images = os.listdir(PATH + "/static/Categories/humans")
    images = ["Categories/humans/" + file for file in images]
    return render_template("category.html", info="humans", images=images)

    # return render_template('category.html',info="humans")


@app.route("/nature")
def nature():

    images = os.listdir(PATH + "/static/Categories/nature")
    images = ["Categories/nature/" + file for file in images]
    return render_template("category.html", info="nature", images=images)

    # return render_template('category.html',info="nature")


@app.route("/other")
def other():

    images = os.listdir(PATH + "/static/Categories/other")
    images = ["Categories/other/" + file for file in images]
    return render_template("category.html", info="other", images=images)

    # return render_template("category.html", info="other")


if __name__ == "__main__":
    app.run()
