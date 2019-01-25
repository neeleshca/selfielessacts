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
    images = os.listdir(PATH + "/static/Categories/Category_0")
    images = ["Categories/Category_0/" + file for file in images]
    return render_template("images.html", images=images)



# @app.route("/user/")
@app.route("/user/<path:thepath>")
def show_user_profile(thepath):
    # print("Username is ",thepath)
    # print("Split is ",thepath.split('/'))
    return render_template("image_single.html",image = thepath)
    # return "User %s" % thepath

@app.route("/<category>")
def category_fun(category):

    print("Category is ",category)
    images = os.listdir(PATH + "/static/Categories/"+category)
    images = ["Categories/"+category+"/" + file for file in images]
    return render_template("category.html", info=category, images=images)


if __name__ == "__main__":
    app.run()
