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
backendIP = "http://127.0.0.1:5001"
os.environ["NO_PROXY"] = '127.0.0.1'


def sorted_images(category):
    #Sorts images in reverse chronological order of modified time

    #Lists all the images
    images = os.listdir(os.path.join(PATH, "static", "Categories", category))
    #Gives the filename which can be used by flask (From static folder)
    images = [os.path.join("Categories", category, file) for file in images]
    images_time = [
        os.path.getmtime(os.path.join(PATH, "static", file)) for file in images
    ]
    sort_list = [list(a) for a in zip(images, images_time)]
    sort_list = sorted(sort_list, reverse=True, key=lambda x: x[1])
    images = [i[0] for i in sort_list]
    return images


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon')


@app.route("/")
def images():
    images = sorted_images("Category_0")
    print(session.get('user'))
    return render_template("images.html", images=images)


@app.route("/add_cat")
def add_cat():
    return render_template('add_cat.html', error=False)


@app.route("/del_cat")
def del_cat():
    resp = requests.get(url=backendIP + '/api/v1/categories')
    return render_template(
        'del_cat.html', category_list=list(resp.json().keys()), error=False)


@app.route("/add_cat_data", methods=['POST'])
def add_cat_data():
    category = request.form.get("category")
    resp = requests.post(url=backendIP + '/api/v1/categories', json=[category])
    if (resp.status_code != 201):
        return render_template('add_cat.html', error=True)
    else:
        return redirect('/category_show')


@app.route('/del_cat_data', methods=['POST'])
def del_cat_data():
    category = request.form.get("category")
    requests.delete(
        url=backendIP + "/api/v1/categories/" + category, json={})
    return redirect('/category_show')


@app.route("/submitted", methods=['POST'])
def submitted():
    resp = requests.post(url=backendIP + '/api/v1/findactid')
    print(resp.json()[0])
    file = request.files["file"]
    category = request.form.get("category")
    caption = request.form.get("caption")
    print("category: ", category)
    print("caption: ", caption)

    req = {
        "actId":
        resp.json()[0],
        "username":
        session['user'],
        "timestamp":
        datetime.datetime.fromtimestamp(
            time.time()).strftime('%d-%m-%Y:%S-%M-%H'),
        "caption":
        caption,
        "categoryName":
        category,
        "imgB64":
        base64.b64encode(file.read()).decode("utf-8")
    }
    resp = requests.post(url=backendIP + '/api/v1/acts', json=req)
    return redirect("/")


@app.route("/delete_user")
def delete_user():
    requests.delete(url=backendIP + "/api/v1/users/" + session['user'])
    return redirect("/logout")


@app.route("/upload")
def upload_page():
    resp = requests.get(url=backendIP + '/api/v1/categories')
    return render_template(
        "upload_page.html", categories=list(resp.json().keys()))


@app.route("/signup")
def signup():
    return render_template("signup.html", error=False)


@app.route("/signupdata", methods=['POST'])
def signupdata():
    username = request.form.get("username")
    passwd = request.form.get("password")
    passwd = hashlib.sha1(passwd.encode('utf-8')).hexdigest()
    req = {"username": username, "password": passwd}
    print(req)
    resp = requests.post(url=backendIP + "/api/v1/users", json=req)
    print(resp)
    if (resp.status_code != 201):
        return render_template("signup.html", error=True)
    else:
        return redirect("/login")


@app.route("/login")
def login():
    return render_template("login.html", error=False)


@app.route("/logindata", methods=['POST'])
def logindata():
    username = request.form.get("username")
    passwd = request.form.get("password")
    passwd = hashlib.sha1(passwd.encode('utf-8')).hexdigest()
    req = {"username": username, "password": passwd}
    print(req)
    resp = requests.post(url=backendIP + "/api/v1/uservalidate", json=req)
    if (resp.status_code != 201):
        return render_template("login.html", error=True)
    else:
        session['user'] = username
        return redirect("/")


@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect("/")


@app.route("/category_show")
def category_show():
    resp = requests.get(url=backendIP + '/api/v1/categories')
    print(list(resp.json().keys()))
    return render_template(
        "category_list.html", category_list=list(resp.json().keys()))




act_set_le100 = None
act_set_g100 = None
startRange = 0
endRange = 0
# @app.route("/user/")
@app.route("/show_single_image/<act_id>")
def show_single_image(act_id):
    print("I AM HEREss")
    global act_set_le100
    global act_set_g100
    print("pls")
    print(type(act_id))
    act_data = 0
    try: 
        act_data = next(act_set_le100[item] for item in range(len(act_set_le100)) if act_set_le100[item]['actId'] == int(act_id))
    except:
        act_data = next(act_set_g100[item] for item in range(len(act_set_g100)) if act_set_g100[item]['actId'] == int(act_id))
    # for i in range(len(act_set_le100.json())):
    #     print(act_set_le100.json()[i]['actId'] )
    #     if(act_set_le100.json()[i]['actId'] == act_id):
    #         print("Please")
    #         act_data = act_set_le100.json()[i]
    #         break
    # print(act_data)

    return render_template("image_single.html", single_datum=act_data)

@app.route("/upvote", methods = ['POST'])
def upvote_front():
    act_id = request.form.get("act_id")
    requests.post(url = backendIP + "/api/v1/acts/upvote", json = [int(act_id)])
    if act_set_le100 is not None:
        for i in range(len(act_set_le100)):
            if(act_set_le100[i]['actId'] == int(act_id)):
                act_set_le100[i]['upvotes']+=1
                break
    if act_set_g100 is not None:
        for i in range(len(act_set_g100)):
            if(act_set_g100[i]['actId'] == int(act_id)):
                act_set_g100[i]['upvotes']+=1
                break
    return redirect("/show_single_image/" + act_id)


@app.route("/deletepage", methods = ['POST'])
def delete_image():
    act_id = request.form.get("act_id")
    print( backendIP + "​/api/v1/acts/" + str(act_id))
    requests.delete(url = backendIP + "​/api/v1/acts/" + str(act_id) , json = {})
    return redirect("/")




@app.route("/<category>")
def category_fun(category):
    # print("Category is ", category)
    resp = requests.get(url=backendIP + '/api/v1/categories/' + category + '/acts/size')
    print(resp.json())
    if (int(resp.json()[0]) <= 100):
        print("length" + str(int(resp.json()[0])))
        global act_set_le100
        act_set_le100 = requests.get(url=backendIP + '/api/v1/categories/' + category + '/acts')
        act_set = act_set_le100
        act_set_data = act_set.json()
        act_set_le100 = act_set_le100.json()
        return render_template("category_le100.html", info=category, datum=act_set_data)
    else:
        startRange = 1
        endRange = 100
        global act_set_g100
        act_set_g100 = requests.get(url=backendIP + '/api/v1/categories/' + category + '/acts?start=' + startRange + '&end=' + endRange)
        act_set = act_set_g100
        act_set_data = act_set.json()
        act_set_g100 = act_set_g100.json()
        return render_template("category_g100.html", info=category, datum=act_set_data)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run()
