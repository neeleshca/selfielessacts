from flask import Flask, request, send_from_directory, jsonify
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


'''
APIs START HERE!!!!!!
'''

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
        a = time.strptime(body["timestamp"],"%d-%m-%Y:%S-%M-%H")
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
    
    toInsert = {"act":{"actID":str(body["actId"]), "username":body["username"],"timestamp":a,
        "caption":body["caption"],"upvotes":0,"imgb64":body["imgB64"],"category":body["categoryName"]
    }}
    db.acts.insert_one(toInsert)
    db.category.update_one({"category.name":body["categoryName"]}, {'$inc':{"category.count":1}})
    return jsonify({}), 201
        

    
@app.route('/api/v1/uservalidate', methods = ['POST'])
def validate_user():
    body = request.get_json()
    print(type(body))
    query = db.users.find_one({"user.username":body["username"]})
    print(query)
    if query is None:
        return jsonify({}), 400
    if query["user"]["password"] != body["password"]:
        return jsonify({}), 400
    else:
        return jsonify({}), 201
    
@app.route('/api/v1/findactid', methods = ['POST'])
def find_actid():
    cursor = db.acts.find().sort('act.actID', pymongo.ASCENDING)
    id = 0
    for i in cursor:
        print(i)
        if(i['act']['actID'] != str(id)):
            break
        id += 1
    return jsonify([id]), 201

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=12345)

