from flask import Flask, render_template, url_for, request, redirect, send_from_directory, jsonify
from inspect import getsourcefile
import os
from os.path import abspath
import random
import pymongo
import time
import base64

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["database"]
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
    body =  request.get_json()
    query = db.acts.find_one({"act.actID":str(body[0])})
    if query is None:
        print("Act Does Not Exist!")
        return jsonify({}), 400    
    db.acts.update_one({"act.actID":str(body[0])}, {'$inc':{"act.upvotes":1}})
    return jsonify({}), 200
    

@app.route("/api/v1/acts/<actID>", methods = ['DELETE'])
def removeAct(actID):
    query = db.acts.find_one({"act.actID":actID})
    if query is None:
        print("Act Does Not Exist!")
        return jsonify({}), 400 
    db.category.update_one({"category.name":query["act"]["category"]}, {'$inc':{"category.count":-1}})
    db.acts.delete_one({"act.actID":actID})
    return jsonify({}), 200
@app.route('/api/v1/acts', methods = ['POST'])
def uploadAct():
    body = request.get_json()
    query = db.acts.find_one({"act.actID":str(body["actId"])})
    if query is not None:
        print("ActID already Exists!")
        return jsonify({}), 400
    try:
        time.strptime(body["timestamp"],"%d-%m-%Y:%S-%M-%H")
    except:
        print("Timestamp format not correct!")
        return jsonify({}), 400
    print(body["username"])
    query = db.users.find_one({"user.username":body["username"]})
    if query is None:
        print("User does not exist!")
        return jsonify({}), 400
    try:
        base64.b64decode(body["imgB64"])
    except:
        print("Image not Base64 Encoded")
        return jsonify({}), 400
    if "upvotes" in body:
        print("No upvotes field is to be set!")
        return jsonify({}), 400
    query = db.category.find_one({"category.name":body["categoryName"]})
    if query is None:
        print("Category does not exist!")
        return jsonify({}), 400
    
    toInsert = {"act":{"actID":str(body["actId"]), "username":body["username"],"timestamp":body["timestamp"],
        "caption":body["caption"],"upvotes":0,"imgb64":body["imgB64"],"category":body["categoryName"]
    }}
    db.acts.insert_one(toInsert)
    db.category.update_one({"category.name":body["categoryName"]}, {'$inc':{"category.count":1}})
    return jsonify({}), 201
        

    



    
if __name__ == "__main__":
    app.run()
