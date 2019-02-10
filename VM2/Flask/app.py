from flask import Flask, request, send_from_directory, jsonify, make_response
from inspect import getsourcefile
import os
from os.path import abspath
import random
import pymongo
import time
import base64
from flask_restful import reqparse, abort, Api, Resource
import json
import re

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["database"]
act = db["acts"]
category = db["category"]
user = db["user"]

app = Flask(__name__)
api = Api(app)

PATH = abspath(getsourcefile(lambda: 0)).rsplit("/", 1)[0]


'''
APIs START HERE!!!!!!
'''

def validate_request(content, input_type, req_len):
    if isinstance(content, (input_type,)) == False:
        return False
    if len(content) != req_len:
        return False


@app.route("/api/v1/acts/upvote", methods = ['POST'])
def upvote():
    body =  request.get_json()
    query = db.acts.find_one({"act.actID":str(body[0])})
    if query is None:
        print("Act Does Not Exist!")
        return jsonify({}), 400    
    db.acts.update_one({"act.actID":str(body[0])}, {'$inc':{"act.upvotes":1}})
    return jsonify({}), 200


def getNumberOfActs(categoryName):
    
    category = db.category.find_one({"category.name":categoryName}) #query for category

    if(category == None): #if category does not exist

        return -1
    
    print(category)
    number = category["category"]["count"] #get size from the returned dictionary
    return number

#get Acts given category

def getActs(categoryName):
    
    acts = db.acts.find({"act.category":categoryName}) #query for acts given the category
    
    return acts


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

@app.route('/api/v1/categories/<categoryName>/acts', methods = ['GET'])
def listActs(categoryName):
    
    startRange = request.args.get("start") #get start parameter
    
    endRange = request.args.get("end") #get end parameter
    
    number = getNumberOfActs(categoryName) #get number of acts of the given category
    
    if(number == -1):
        
        return jsonify({}), 405  #method not allowed if category does not exist
    
    if(number == 0):
        
        return jsonify({}), 204  #no content if no acts under existing category
    
    if(startRange == None and endRange == None):   #if API 6 
        
        if(number < 100):
            
            acts = getActs(categoryName)

            if(len(acts) == 0):
                return jsonify({}), 204
            
            actsList = []
            
            for i in acts:
                print(i)
            
                i.pop("_id")   #remove the Mongo-DB's in-built ObjectId attribute
            
                i["act"]["timestamp"] = time.strftime('%Y-%m-%dT%H:%M:%SZ', tuple(i["act"]["timestamp"]))
                #i["act"]["timestamp"][0] = i["act"]["timestamp"][0].strftime("%Y-%m-%d:%S:%M:%H") #convert timestamp to string for json conversion
            
                actsList.append(i)
            
            response = json.dumps(actsList)
            
            return response, 200
        
        else:
        
            return jsonify({}), 413  #if number of acts in the given category is > 100 (Payload too large)
    
    else: #if API 8
        startRange = int(startRange)
        
        endRange = int(endRange)
        
        if(endRange-startRange+1 > 100):
            
            return jsonify({}), 413  #payload to large - range > 100

        if(startRange < 1 or endRange > number): #if invalid range, method not allowed
            
            return jsonify({}), 405
        
        acts = getActs(categoryName).sort("act.timestamp",-1) #sort in descending order of timestamp (latest first)
        
        tempList = []
        
        actsList = []
        
        for i in acts: #since acts object is not indexable, create a tempList
            
            tempList.append(i)

        if(len(tempList) == 0):

            return jsonify({}), 204

        if(startRange < 1 or endRange > len(tempList)):
            
            return jsonify({}), 405
        
        for i in range(startRange-1,endRange-1):
            
            tempList[i].pop("_id")
            
            tempList[i]["act"]["timestamp"] = time.strftime('%Y-%m-%dT%H:%M:%SZ', tuple(tempList[i]["act"]["timestamp"]))
            
            actsList.append(tempList[i])
        
        response = json.dumps(actsList)
        
        return response, 200


@app.route('/api/v1/categories/<categoryName>/acts/size', methods = ['GET'])
def getNumberOfActsGivenCategory(categoryName):
    
    number = getNumberOfActs(categoryName)
    
    if(number == -1):
    
        return jsonify({}), 405
    
    elif(number == 0):
        
        return jsonify({}), 204
    
    return jsonify([number]), 200

    
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

# API's 3-5
class Category(Resource):
    def get(self):
        # print("Inside here\n")
        x = category.find({})
        dict1 = {i["category"]["name"]: i["category"]["count"] for i in x}
        if len(dict1) == 0:
            return make_response(jsonify({}), 204)
        # response = app.response_class(
        #     response=json.dumps(y), mimetype='application/json')
        
        # return jsonify(dict1)
        return make_response(jsonify(dict1),200)
        

    def post(self):
        # print("Self",self)
        # print("Resource is ", str(Resource))
        # print("Self ifs", str(self))
        try:
            content = request.json
        except:
            return make_response(jsonify({}),400)

        if validate_request(content, list, 1) == False:
            return make_response(jsonify({}),400)


        temp = category.find_one({"category.name": content[0]})
        # print("Temp is",temp)
        # print("Temp is ", type((temp)))
        if temp is not None:
            return make_response(jsonify({}),400)

        dict_temp = {"category": {"name": content[0], "count": 0}}
        # print(content)
        # print(type(content))
        category.insert(dict_temp)
        return make_response(jsonify({}),201)

    def delete(self, del_arg):
        temp = category.delete_one({"category.name": del_arg})

        if temp.deleted_count == 0:
            return make_response(jsonify({}),400)
            
        act.delete_many({"act.category": del_arg})
        # print(xyz)
        return make_response(jsonify({}),200)

# API's 1-2
class User(Resource):
        
    # Adding an user
    def post(self):
        try:
            content = request.json
        except:
            return make_response(jsonify({}),400)

        if (validate_request(content, list, 1) == False):
            return make_response(jsonify({}),400)

        # user already existing case
        query = user.find_one({"user.username": content[0]})
        if query is not None:
            return make_response(jsonify({}),400)

        regex = re.compile('^[a-fA-F0-9]{40}$')
        if (not(regex.match(content[1]))):
            return make_response(jsonify({}), 400)

        dict_temp = {"user": {"username": content[0], "password": content[1]}}
        user.insert(dict_temp)
        return make_response(jsonify({}),201)

    # Removing an user
    def delete(self, del_arg):
        query = user.delete_one({"user.username": del_arg})
        # user does not exist to be deleted
        if (query.deleted_count == 0):
            return make_response(jsonify({}),400)
        return make_response(jsonify({}),200)


api.add_resource(User, '/api/v1/users', '/api/v1/users/<del_arg>')
api.add_resource(Category, "/api/v1/categories", "/api/v1/categories/<del_arg>")

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)
 