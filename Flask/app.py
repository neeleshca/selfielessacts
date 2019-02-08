from flask import Flask, render_template, url_for, request, redirect, send_from_directory, jsonify
from inspect import getsourcefile
import os
from os.path import abspath
import random
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["db"]
app = Flask(__name__)
PATH = abspath(getsourcefile(lambda: 0)).rsplit("/", 1)[0]

def sorted_images(category):
    #Sorts images in reverse chronological order of modified time

    #Lists all the images
    images = os.listdir(os.path.join(PATH, "static", "Categories", category))
    #Gives the filename which can be used by flask (From static folder)
    images = [os.path.join("Categories",category,file) for file in images]
    images_time = [os.path.getmtime(os.path.join(PATH, "static", file)) for file in images]
    sort_list = [list(a) for a in zip(images, images_time)]
    sort_list = sorted(sort_list, reverse=True, key=lambda x: x[1])
    images = [i[0] for i in sort_list]
    return images

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/")
def images():
    images = sorted_images("Category_0")
    return render_template("images.html", images=images)

@app.route("/submitted", methods = ['POST'])
def submitted():
    file = request.files["file"]
    category = request.form.get("category")
    caption = request.form.get("caption")
    print("category: ", category)
    print("caption: ", caption)
    target = os.path.join(PATH, "static", "Categories", category, caption)
    file.save(target)   
    return redirect("/")

@app.route("/upload")
def upload_page():
    return render_template("upload_page.html")

@app.route("/deleted", methods = ['POST'])
def deleted():
    filePath = request.form.get("Delete")
    filePath = os.path.join(PATH, "static", filePath)

    #print(filePath)
    os.remove(filePath)
    return redirect("/")

# @app.route("/user/")
@app.route("/<path:thepath>")
def show_single_image(thepath):
    temp = thepath.rsplit('/')[-1]
    caption = temp.rsplit('.')[0]
    # print(thepath)
    return render_template("image_single.html", image=thepath, caption = caption)



@app.route("/<category>")
def category_fun(category):
    # print("Category is ", category)
    images = sorted_images(category)
    return render_template("category.html", info=category, images=images)
@app.route("/api/v1/acts/upvote", methods = ['POST'])
def upvote():
    try:
        body =  request.get_json()
        query = db.Acts.find({str(body[0]):{'$exists':True}})
        for i in query:
            print(i)
        if(query.retrieved == 0):
            raise FileNotFoundError
        if(query.retrieved != 1):
            raise FileExistsError
        db.Acts.update({str(body[0]):{'$exists':True}}, {'$inc':{str(body[0]) + ".upvotes":1}})
        return jsonify({}), 200
    except Exception as e:
        print("Failed Outside")
        print(e)
        return jsonify({}), 400
        
if __name__ == "__main__":
    app.run()
