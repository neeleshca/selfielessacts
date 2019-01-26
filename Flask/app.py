from flask import Flask, render_template, url_for
from inspect import getsourcefile
import os
from os.path import abspath


app = Flask(__name__)
PATH = abspath(getsourcefile(lambda: 0)).rsplit("/", 1)[0]


def sorted_images(category):
    images = os.listdir(PATH + "/static/Categories/" + category)
    images = ["Categories/" + category + "/" + file for file in images]
    images_time = [os.path.getmtime(PATH + "/static/" + file) for file in images]
    sort_list = [list(a) for a in zip(images, images_time)]
    sort_list = sorted(sort_list, reverse=True, key=lambda x: x[1])
    images = [i[0] for i in sort_list]
    return images


@app.route("/")
def images():
    images = sorted_images("Category_0")
    return render_template("images.html", images=images)


# @app.route("/user/")
@app.route("/<path:thepath>")
def show_user_profile(thepath):
    return render_template("image_single.html", image=thepath)



@app.route("/<category>")
def category_fun(category):
    print("Category is ", category)
    images = sorted_images(category)
    return render_template("category.html", info=category, images=images)


if __name__ == "__main__":
    app.run()
