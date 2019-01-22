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
    





if __name__ == "__main__":
    app.run()
