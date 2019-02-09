from flask import Flask, render_template, url_for, request, redirect, send_from_directory, jsonify, session
from inspect import getsourcefile
import os
from os.path import abspath
import random
import time
import datetime
import base64
import requests
import hashlib
import json

app = Flask(__name__)
PATH = abspath(getsourcefile(lambda: 0)).rsplit("/", 1)[0]
backendIP = "http://127.0.0.1:12345"
os.environ["NO_PROXY"] = '127.0.0.1'
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
    print(session.get('user'))
    return render_template("images.html", images=images)

@app.route("/submitted", methods = ['POST'])
def submitted():
    resp = requests.post(url = backendIP + '/api/v1/findactid')
    print(resp.json()[0])
    file = request.files["file"]
    category = request.form.get("category")
    caption = request.form.get("caption")
    print("category: ", category)
    print("caption: ", caption)

    req = {
        "actId": resp.json()[0],
        "username": session['user'],
        "timestamp": datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y:%S-%M-%H'),
        "caption": caption,
        "categoryName": category,
        "imgB64":base64.b64encode(file.read()).decode("utf-8") 
    }
    resp = requests.post(url = backendIP + '/api/v1/acts', json = req)
    return redirect("/")

@app.route("/delete_user")
def delete_user():
    requests.delete(url = backendIP + session['username'])
    return redirect("/logout")

@app.route("/upload")
def upload_page():
    resp = requests.get(url = backendIP + '/api/v1/categories')    
    return render_template("upload_page.html", categories = list(resp.json().keys))
@app.route("/signup")
def signup():
    return render_template("signup.html", error = False)
@app.route("/signupdata", methods = ['POST'])
def signupdata():
    username = request.form.get("username")
    passwd = request.form.get("password")
    passwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    req = {"username":username,"password":passwd}
    print(req)
    req = json.dumps(req)
    resp = requests.post(url = backendIP + "/api/v1/users", json = req)
    print(resp)
    if(resp.status_code != 201):
        return render_template("signup.html", error = True)
    else:
        return redirect("/login")
@app.route("/login")
def login():
    return render_template("login.html", error = False)

@app.route("/logindata", methods=['POST'])
def logindata():
    username = request.form.get("username")
    passwd = request.form.get("password")
    passwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    req = {"username":username,"password":passwd}
    print(req)
    resp = requests.post(url = backendIP + "/api/v1/uservalidate", json = req)
    if(resp.status_code != 201):
        return render_template("login.html", error = True)
    else:
        session['user'] = username
        return redirect("/")
@app.route("/logout")
def logout():
    session.pop('user', None)     
    return redirect("/")
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



    
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run()
